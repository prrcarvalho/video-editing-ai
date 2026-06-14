# Freesound MCP Server

An MCP (Model Context Protocol) server that provides access to the Freesound API, enabling AI assistants to search, analyze, and retrieve information about audio samples from Freesound.org.

## Prerequisites

- Node.js 16 or higher
- A Freesound API key (get one at https://freesound.org/apiv2/apply)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd freesound-mcp-server
```

2. Install dependencies:
```bash
npm install
```

3. Build the project:
```bash
npm run build
```

## Quick Start with Claude Code

### Global Installation (All Projects)

1. Get your Freesound API key from https://freesound.org/apiv2/apply

3. Add to Claude Code:
```bash
# From the freesound-mcp-server directory (user scope for global access)
claude mcp add freesound -e FREESOUND_API_KEY=your-api-key-here -- node /path/to/freesound-mcp-server/dist/index.js
```

### Verifying Installation

To check if the MCP server is properly configured and running, use the `/mcp` command in Claude Code:

```bash
claude
> /mcp
```

This will show the status of all configured MCP servers.

## Usage with Claude Desktop

Add the following to your Claude Desktop configuration file:

### macOS
`~/Library/Application Support/Claude/claude_desktop_config.json`

### Windows
`%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "freesound": {
      "command": "node",
      "args": ["/path/to/freesound-mcp-server/dist/index.js"],
      "env": {
        "FREESOUND_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

## Available Tools

### search_sounds
Search for sounds on Freesound using text queries.

Parameters:
- `query` (required): Search query terms
- `filter`: Filter using Solr syntax (e.g., "duration:[1 TO 5]")
- `sort`: Sort results by various criteria
- `page`: Page number (default: 1)
- `page_size`: Results per page (default: 15, max: 150)

Example:
```
Search for: "piano jazz" with filter "duration:[5 TO 30]" sorted by "downloads_desc"
```

### get_sound
Get detailed information about a specific sound.

Parameters:
- `sound_id` (required): The ID of the sound
- `descriptors`: Comma-separated list of content descriptors to include

### get_sound_analysis
Retrieve audio analysis data for a sound.

Parameters:
- `sound_id` (required): The ID of the sound
- `descriptors`: Specific analysis descriptors to retrieve
- `normalized`: Whether to normalize descriptor values

### get_similar_sounds
Find sounds similar to a given sound.

Parameters:
- `sound_id` (required): The ID of the reference sound
- `descriptors_filter`: Filter by content descriptors
- `page`: Page number
- `page_size`: Results per page

### get_user
Get information about a Freesound user.

Parameters:
- `username` (required): The username

### get_user_sounds
Get sounds uploaded by a specific user.

Parameters:
- `username` (required): The username
- `page`: Page number
- `page_size`: Results per page

### get_pack
Get information about a sound pack.

Parameters:
- `pack_id` (required): The ID of the pack

### get_pack_sounds
Get sounds from a specific pack.

Parameters:
- `pack_id` (required): The ID of the pack
- `page`: Page number
- `page_size`: Results per page

## Development

Run the server in development mode:
```bash
npm run dev
```

## API Limitations

- Token authentication is used for most endpoints
- OAuth2 is required for downloading sounds and write operations (not implemented in this version)
- Rate limits apply based on your Freesound API plan
- Maximum page size is 150 results

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues with the Freesound API, consult:
- Freesound API Documentation: https://freesound.org/docs/api/
- Freesound API Forum: https://freesound.org/forum/

For issues with this MCP server, please open an issue on GitHub.