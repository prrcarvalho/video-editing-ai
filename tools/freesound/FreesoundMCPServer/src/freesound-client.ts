import axios, { AxiosInstance } from 'axios';

export interface SearchParams {
  query: string;
  filter?: string;
  sort?: string;
  page?: number;
  page_size?: number;
  group_by_pack?: boolean;
}

export interface PaginationParams {
  page?: number;
  page_size?: number;
}

export interface SimilarSoundsParams extends PaginationParams {
  descriptors_filter?: string;
}

export interface Sound {
  id: number;
  url: string;
  name: string;
  tags: string[];
  description: string;
  geotag: string | null;
  created: string;
  license: string;
  type: string;
  channels: number;
  filesize: number;
  bitrate: number;
  bitdepth: number;
  duration: number;
  samplerate: number;
  username: string;
  pack: string | null;
  pack_name: string | null;
  download: string;
  bookmark: string;
  previews: {
    [key: string]: string;
  };
  images: {
    waveform_m: string;
    waveform_l: string;
    spectral_m: string;
    spectral_l: string;
  };
  num_downloads: number;
  avg_rating: number;
  num_ratings: number;
  rate: string;
  comments: string;
  num_comments: number;
  comment: string;
  similar_sounds: string;
  analysis: string;
  analysis_frames: string;
  analysis_stats: string;
  [key: string]: any;
}

export interface User {
  url: string;
  username: string;
  about: string;
  home_page: string;
  avatar: {
    small: string;
    medium: string;
    large: string;
  };
  date_joined: string;
  num_sounds: number;
  sounds: string;
  num_packs: number;
  packs: string;
  num_posts: number;
  num_comments: number;
  bookmark_categories: string;
}

export interface Pack {
  id: number;
  url: string;
  description: string;
  created: string;
  name: string;
  username: string;
  num_sounds: number;
  sounds: string;
  num_downloads: number;
}

export interface SearchResults {
  count: number;
  next: string | null;
  previous: string | null;
  results: Sound[];
}

export interface PaginatedResults<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export class FreesoundClient {
  private axiosInstance: AxiosInstance;
  private apiKey: string;

  constructor(apiKey: string) {
    this.apiKey = apiKey;
    this.axiosInstance = axios.create({
      baseURL: 'https://freesound.org/apiv2',
      headers: {
        'Authorization': `Token ${apiKey}`,
      },
    });
  }

  async searchSounds(params: SearchParams): Promise<SearchResults> {
    const response = await this.axiosInstance.get('/search/text/', {
      params: {
        query: params.query,
        filter: params.filter,
        sort: params.sort,
        page: params.page || 1,
        page_size: params.page_size || 15,
        group_by_pack: params.group_by_pack ? 1 : 0,
      },
    });
    return response.data;
  }

  async getSound(soundId: number, descriptors?: string): Promise<Sound> {
    const response = await this.axiosInstance.get(`/sounds/${soundId}/`, {
      params: {
        descriptors: descriptors,
      },
    });
    return response.data;
  }

  async getSoundAnalysis(
    soundId: number,
    descriptors?: string,
    normalized?: boolean
  ): Promise<any> {
    const response = await this.axiosInstance.get(
      `/sounds/${soundId}/analysis/`,
      {
        params: {
          descriptors: descriptors,
          normalized: normalized !== undefined ? (normalized ? 1 : 0) : undefined,
        },
      }
    );
    return response.data;
  }

  async getSimilarSounds(
    soundId: number,
    params?: SimilarSoundsParams
  ): Promise<PaginatedResults<Sound>> {
    const response = await this.axiosInstance.get(
      `/sounds/${soundId}/similar/`,
      {
        params: {
          descriptors_filter: params?.descriptors_filter,
          page: params?.page || 1,
          page_size: params?.page_size || 15,
        },
      }
    );
    return response.data;
  }

  async downloadSound(soundId: number): Promise<string> {
    const response = await this.axiosInstance.get(
      `/sounds/${soundId}/download/`,
      {
        responseType: 'stream',
      }
    );
    return response.headers['location'] || response.data;
  }

  async getUser(username: string): Promise<User> {
    const response = await this.axiosInstance.get(`/users/${username}/`);
    return response.data;
  }

  async getUserSounds(
    username: string,
    params?: PaginationParams
  ): Promise<PaginatedResults<Sound>> {
    const response = await this.axiosInstance.get(
      `/users/${username}/sounds/`,
      {
        params: {
          page: params?.page || 1,
          page_size: params?.page_size || 15,
        },
      }
    );
    return response.data;
  }

  async getUserPacks(
    username: string,
    params?: PaginationParams
  ): Promise<PaginatedResults<Pack>> {
    const response = await this.axiosInstance.get(`/users/${username}/packs/`, {
      params: {
        page: params?.page || 1,
        page_size: params?.page_size || 15,
      },
    });
    return response.data;
  }

  async getPack(packId: number): Promise<Pack> {
    const response = await this.axiosInstance.get(`/packs/${packId}/`);
    return response.data;
  }

  async getPackSounds(
    packId: number,
    params?: PaginationParams
  ): Promise<PaginatedResults<Sound>> {
    const response = await this.axiosInstance.get(`/packs/${packId}/sounds/`, {
      params: {
        page: params?.page || 1,
        page_size: params?.page_size || 15,
      },
    });
    return response.data;
  }

  async commentSound(soundId: number, comment: string): Promise<any> {
    const response = await this.axiosInstance.post(
      `/sounds/${soundId}/comment/`,
      { comment }
    );
    return response.data;
  }

  async rateSound(soundId: number, rating: number): Promise<any> {
    if (rating < 0 || rating > 5) {
      throw new Error('Rating must be between 0 and 5');
    }
    const response = await this.axiosInstance.post(
      `/sounds/${soundId}/rate/`,
      { rating }
    );
    return response.data;
  }

  async bookmarkSound(
    soundId: number,
    name?: string,
    category?: string
  ): Promise<any> {
    const response = await this.axiosInstance.post(
      `/sounds/${soundId}/bookmark/`,
      { name, category }
    );
    return response.data;
  }

  async uploadSound(formData: FormData): Promise<any> {
    const response = await this.axiosInstance.post('/sounds/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }
}