import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useSetAtom } from 'jotai';
import api from '../api';
import { tokenAtom, userAtom, User } from '../store/auth-store';

export const useAuth = () => {
    const setToken = useSetAtom(tokenAtom);
    const setUser = useSetAtom(userAtom);
    const queryClient = useQueryClient();

    const loginMutation = useMutation({
        mutationFn: async (credentials: any) => {
            const { data } = await api.post('/auth/login', credentials);
            return data;
        },
        onSuccess: (data) => {
            setToken(data.access_token);
            localStorage.setItem('apollo_token', data.access_token);
            setUser(data.user);
            queryClient.setQueryData(['user'], data.user);
        },
    });

    const signupMutation = useMutation({
        mutationFn: async (userData: any) => {
            const { data } = await api.post('/auth/register', userData);
            return data;
        },
        onSuccess: (data) => {
            setToken(data.access_token);
            localStorage.setItem('apollo_token', data.access_token);
            setUser(data.user);
            queryClient.setQueryData(['user'], data.user);
        },
    });

    const useUser = (enabled: boolean = true) => {
        return useQuery({
            queryKey: ['user'],
            queryFn: async () => {
                const { data } = await api.get<User>('/auth/me');
                setUser(data);
                return data;
            },
            enabled,
        });
    };

    const logout = () => {
        setToken(null);
        localStorage.removeItem('apollo_token');
        setUser(null);
        queryClient.clear();
    };

    return {
        login: loginMutation.mutateAsync,
        isLoggingIn: loginMutation.isPending,
        signup: signupMutation.mutateAsync,
        isSigningUp: signupMutation.isPending,
        useUser,
        logout,
    };
};
