import { Metadata } from 'next';
import { redirect } from 'next/navigation';

export const metadata: Metadata = {
  title: 'Agent Conversation | Kortix ChromaFlow Agent',
  description: 'Interactive agent conversation powered by Kortix ChromaFlow Agent',
  openGraph: {
    title: 'Agent Conversation | Kortix ChromaFlow Agent',
    description: 'Interactive agent conversation powered by Kortix ChromaFlow Agent',
    type: 'website',
  },
};

export default async function AgentsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
}
