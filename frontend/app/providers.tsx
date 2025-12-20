'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useAtomValue, useSetAtom } from 'jotai';
import { ReactNode, useEffect, useState } from 'react';
import { tokenAtom, userAtom } from './lib/store/auth-store';
import { useAuth } from './lib/hooks/auth-hooks';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
      refetchOnWindowFocus: false,
    },
  },
});

function AuthInitializer({ children }: { children: ReactNode }) {
  const token = useAtomValue(tokenAtom);
  const setUser = useSetAtom(userAtom);
  const { useUser } = useAuth();
  const [mounted, setMounted] = useState(false);

  // We only want to fetch the user if we have a token
  const { data: userData, isSuccess } = useUser(!!token);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (isSuccess && userData) {
      setUser(userData as any);
    }
  }, [isSuccess, userData, setUser]);

  if (!mounted) return null;

  return <>{children}</>;
}

export function Providers({ children }: { children: ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthInitializer>{children}</AuthInitializer>
    </QueryClientProvider>
  );
}
