#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ErrorCode,
  ListToolsRequestSchema,
  McpError,
} from "@modelcontextprotocol/sdk/types.js";
import { FreesoundClient } from "./freesound-client.js";

const server = new Server(
  {
    name: "freesound-mcp",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

const API_KEY = process.env.FREESOUND_API_KEY;
if (!API_KEY) {
  console.error("Error: FREESOUND_API_KEY environment variable is required");
  process.exit(1);
}

const freesoundClient = new FreesoundClient(API_KEY);

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "search_sounds",
        description: "Search for sounds on Freesound using text queries",
        inputSchema: {
          type: "object",
          properties: {
            query: {
              type: "string",
              description: "Search query terms",
            },
            filter: {
              type: "string",
              description: "Filter query using Solr syntax (e.g., 'duration:[1 TO 5]')",
            },
            sort: {
              type: "string",
              description: "Sort results by: score, duration_desc, duration_asc, created_desc, created_asc, downloads_desc, downloads_asc, rating_desc, rating_asc",
              enum: ["score", "duration_desc", "duration_asc", "created_desc", "created_asc", "downloads_desc", "downloads_asc", "rating_desc", "rating_asc"],
            },
            page: {
              type: "number",
              description: "Page number (default: 1)",
            },
            page_size: {
              type: "number",
              description: "Number of results per page (default: 15, max: 150)",
            },
          },
          required: ["query"],
        },
      },
      {
        name: "get_sound",
        description: "Get detailed information about a specific sound",
        inputSchema: {
          type: "object",
          properties: {
            sound_id: {
              type: "number",
              description: "The ID of the sound",
            },
            descriptors: {
              type: "string",
              description: "Comma-separated list of content-based descriptors to include",
            },
          },
          required: ["sound_id"],
        },
      },
      {
        name: "get_sound_analysis",
        description: "Get audio analysis data for a specific sound",
        inputSchema: {
          type: "object",
          properties: {
            sound_id: {
              type: "number",
              description: "The ID of the sound",
            },
            descriptors: {
              type: "string",
              description: "Comma-separated list of analysis descriptors to retrieve",
            },
            normalized: {
              type: "boolean",
              description: "Whether to normalize descriptor values",
            },
          },
          required: ["sound_id"],
        },
      },
      {
        name: "get_similar_sounds",
        description: "Find sounds similar to a given sound",
        inputSchema: {
          type: "object",
          properties: {
            sound_id: {
              type: "number",
              description: "The ID of the sound to find similar sounds for",
            },
            descriptors_filter: {
              type: "string",
              description: "Filter similar sounds by content descriptors",
            },
            page: {
              type: "number",
              description: "Page number (default: 1)",
            },
            page_size: {
              type: "number",
              description: "Number of results per page (default: 15)",
            },
          },
          required: ["sound_id"],
        },
      },
      {
        name: "get_user",
        description: "Get information about a Freesound user",
        inputSchema: {
          type: "object",
          properties: {
            username: {
              type: "string",
              description: "The username of the user",
            },
          },
          required: ["username"],
        },
      },
      {
        name: "get_user_sounds",
        description: "Get sounds uploaded by a specific user",
        inputSchema: {
          type: "object",
          properties: {
            username: {
              type: "string",
              description: "The username of the user",
            },
            page: {
              type: "number",
              description: "Page number (default: 1)",
            },
            page_size: {
              type: "number",
              description: "Number of results per page (default: 15)",
            },
          },
          required: ["username"],
        },
      },
      {
        name: "get_pack",
        description: "Get information about a sound pack",
        inputSchema: {
          type: "object",
          properties: {
            pack_id: {
              type: "number",
              description: "The ID of the pack",
            },
          },
          required: ["pack_id"],
        },
      },
      {
        name: "get_pack_sounds",
        description: "Get sounds from a specific pack",
        inputSchema: {
          type: "object",
          properties: {
            pack_id: {
              type: "number",
              description: "The ID of the pack",
            },
            page: {
              type: "number",
              description: "Page number (default: 1)",
            },
            page_size: {
              type: "number",
              description: "Number of results per page (default: 15)",
            },
          },
          required: ["pack_id"],
        },
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    const { name, arguments: args = {} } = request.params;

    switch (name) {
      case "search_sounds": {
        const results = await freesoundClient.searchSounds({
          query: args.query as string,
          filter: args.filter as string | undefined,
          sort: args.sort as string | undefined,
          page: args.page as number | undefined,
          page_size: args.page_size as number | undefined,
        });
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(results, null, 2),
            },
          ],
        };
      }

      case "get_sound": {
        const sound = await freesoundClient.getSound(
          args.sound_id as number,
          args.descriptors as string | undefined
        );
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(sound, null, 2),
            },
          ],
        };
      }

      case "get_sound_analysis": {
        const analysis = await freesoundClient.getSoundAnalysis(
          args.sound_id as number,
          args.descriptors as string | undefined,
          args.normalized as boolean | undefined
        );
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(analysis, null, 2),
            },
          ],
        };
      }

      case "get_similar_sounds": {
        const similar = await freesoundClient.getSimilarSounds(
          args.sound_id as number,
          {
            descriptors_filter: args.descriptors_filter as string | undefined,
            page: args.page as number | undefined,
            page_size: args.page_size as number | undefined,
          }
        );
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(similar, null, 2),
            },
          ],
        };
      }

      case "get_user": {
        const user = await freesoundClient.getUser(args.username as string);
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(user, null, 2),
            },
          ],
        };
      }

      case "get_user_sounds": {
        const sounds = await freesoundClient.getUserSounds(
          args.username as string,
          {
            page: args.page as number | undefined,
            page_size: args.page_size as number | undefined,
          }
        );
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(sounds, null, 2),
            },
          ],
        };
      }

      case "get_pack": {
        const pack = await freesoundClient.getPack(args.pack_id as number);
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(pack, null, 2),
            },
          ],
        };
      }

      case "get_pack_sounds": {
        const sounds = await freesoundClient.getPackSounds(
          args.pack_id as number,
          {
            page: args.page as number | undefined,
            page_size: args.page_size as number | undefined,
          }
        );
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(sounds, null, 2),
            },
          ],
        };
      }

      default:
        throw new McpError(
          ErrorCode.MethodNotFound,
          `Unknown tool: ${name}`
        );
    }
  } catch (error) {
    if (error instanceof McpError) {
      throw error;
    }
    throw new McpError(
      ErrorCode.InternalError,
      `Error calling tool ${request.params.name}: ${error}`
    );
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});