import { atom } from 'jotai';
import { atomWithStorage } from 'jotai/utils';

export interface User {
    id: number;
    email: string;
    user_name?: string;
    created_at?: string;
}

// Persistent token atom
export const tokenAtom = atomWithStorage<string | null>('apollo_token', null);

// User atom (can be fetched/updated based on token)
export const userAtom = atom<User | null>(null);

// Auth status atom
export const isAuthenticatedAtom = atom((get) => !!get(tokenAtom));
