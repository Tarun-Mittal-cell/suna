import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'API Keys | ChromaFlow Agent',
  description: 'Manage your API keys for programmatic access to ChromaFlow Agent',
  openGraph: {
    title: 'API Keys | ChromaFlow Agent',
    description: 'Manage your API keys for programmatic access to ChromaFlow Agent',
    type: 'website',
  },
};

export default async function APIKeysLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
}
