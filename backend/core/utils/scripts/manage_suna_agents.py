#!/usr/bin/env python3
"""
ChromaFlow Agent Default Agent Management Script (Simplified)

This script provides administrative functions for managing ChromaFlow Agent default agents across all users.

Usage:
    # 🚀 MAIN COMMANDS
    python manage_chromaflow_agent_agents.py install-all          # Install ChromaFlow Agent for all users who don't have it
    python manage_chromaflow_agent_agents.py stats                # Show ChromaFlow Agent agent statistics
    python manage_chromaflow_agent_agents.py install-user <id>    # Install ChromaFlow Agent for specific user

Examples:
    python manage_chromaflow_agent_agents.py install-all
    python manage_chromaflow_agent_agents.py stats
    python manage_chromaflow_agent_agents.py install-user 123e4567-e89b-12d3-a456-426614174000

Note: Sync is no longer needed - ChromaFlow Agent agents automatically use the current configuration from config.py
"""

import asyncio
import argparse
import sys
import json
from pathlib import Path

# Add the backend directory to the path so we can import modules
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from core.utils.chromaflow_agent_default_agent_service import ChromaFlow AgentDefaultAgentService
from core.services.supabase import DBConnection
from core.utils.logger import logger


class ChromaFlow AgentAgentManager:
    def __init__(self):
        self.service = ChromaFlow AgentDefaultAgentService()
    
    async def install_all_users(self):
        """Install ChromaFlow Agent agent for all users who don't have it"""
        print("🚀 Installing ChromaFlow Agent default agent for all users who don't have it...")
        
        result = await self.service.install_for_all_users()
        
        print(f"✅ Installation completed!")
        print(f"   📦 Installed: {result['installed_count']}")
        print(f"   ❌ Failed: {result['failed_count']}")
        
        if result['failed_count'] > 0:
            print("\n❌ Failed installations:")
            for detail in result['details']:
                if detail['status'] == 'failed':
                    print(f"   - User {detail['account_id']}: {detail.get('error', 'Unknown error')}")
        
        if result['installed_count'] > 0:
            print(f"\n✅ Successfully installed ChromaFlow Agent for {result['installed_count']} users")
            
    async def update_config_info(self):
        """Show information about ChromaFlow Agent configuration (no sync needed)"""
        print("ℹ️  ChromaFlow Agent Configuration Information")
        print("=" * 50)
        print("🔧 ChromaFlow Agent agents automatically use the current configuration from config.py")
        print("📝 No sync needed - changes are applied immediately when agents run")
        print("💡 To update ChromaFlow Agent behavior, simply modify backend/agent/chromaflow_agent/config.py")
        print("\n✅ All ChromaFlow Agent agents are always up-to-date with your latest configuration!")
    
    async def install_user(self, account_id):
        """Install ChromaFlow Agent agent for specific user"""
        print(f"🚀 Installing ChromaFlow Agent default agent for user {account_id}...")
        
        agent_id = await self.service.install_chromaflow_agent_agent_for_user(account_id)
        
        if agent_id:
            print(f"✅ Successfully installed ChromaFlow Agent agent {agent_id} for user {account_id}")
        else:
            print(f"❌ Failed to install ChromaFlow Agent agent for user {account_id}")
    
    async def replace_user_agent(self, account_id):
        """Replace ChromaFlow Agent agent for specific user (in case of corruption)"""
        print(f"🔄 Replacing ChromaFlow Agent agent for user {account_id}...")
        
        # Install/replace the agent with latest config
        agent_id = await self.service.install_chromaflow_agent_agent_for_user(account_id, replace_existing=True)
        
        if agent_id:
            print(f"✅ Successfully replaced ChromaFlow Agent agent {agent_id} for user {account_id}")
        else:
            print(f"❌ Failed to replace ChromaFlow Agent agent for user {account_id}")
    
    async def show_stats(self):
        """Show ChromaFlow Agent agent statistics"""
        print("📊 ChromaFlow Agent Default Agent Statistics")
        print("=" * 50)
        
        stats = await self.service.get_chromaflow_agent_agent_stats()
        
        if 'error' in stats:
            print(f"❌ Error getting stats: {stats['error']}")
            return
        
        print(f"Total Agents: {stats.get('total_agents', 0)}")
        print(f"Active Agents: {stats.get('active_agents', 0)}")
        print(f"Inactive Agents: {stats.get('inactive_agents', 0)}")
        
        version_dist = stats.get('version_distribution', {})
        if version_dist:
            print(f"\nVersion Distribution:")
            for version, count in version_dist.items():
                print(f"  {version}: {count} agents")
        
        creation_dates = stats.get('creation_dates', {})
        if creation_dates:
            print(f"\nCreation Dates (Last 12 months):")
            for month, count in sorted(creation_dates.items(), reverse=True):
                print(f"  {month}: {count} agents")


async def main():
    parser = argparse.ArgumentParser(
        description="Manage ChromaFlow Agent default agents across all users (Simplified)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Main commands
    subparsers.add_parser('install-all', help='Install ChromaFlow Agent agent for all users who don\'t have it')
    subparsers.add_parser('stats', help='Show ChromaFlow Agent agent statistics')
    subparsers.add_parser('config-info', help='Show information about ChromaFlow Agent configuration')
    
    # User-specific commands
    install_user_parser = subparsers.add_parser('install-user', help='Install ChromaFlow Agent agent for specific user')
    install_user_parser.add_argument('account_id', help='Account ID to install ChromaFlow Agent for')
    
    replace_user_parser = subparsers.add_parser('replace-user', help='Replace ChromaFlow Agent agent for specific user (if corrupted)')
    replace_user_parser.add_argument('account_id', help='Account ID to replace ChromaFlow Agent for')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = ChromaFlow AgentAgentManager()
    
    try:
        if args.command == 'install-all':
            await manager.install_all_users()
        elif args.command == 'stats':
            await manager.show_stats()
        elif args.command == 'config-info':
            await manager.update_config_info()
        elif args.command == 'install-user':
            await manager.install_user(args.account_id)
        elif args.command == 'replace-user':
            await manager.replace_user_agent(args.account_id)
        else:
            parser.print_help()
            
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        logger.error(f"Script error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main()) 