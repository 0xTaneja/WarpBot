#!/usr/bin/env python
"""Command-line interface for the SDK."""

import asyncio
import json
import os
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from sdkwarp.client import Client
from sdkwarp.config.models import ChainEnv

# Create console for pretty output
console = Console()

# Create Typer application
app = typer.Typer(help="Command-line interface for the SDK")


def get_client(
    env: Optional[str] = None,
    address: Optional[str] = None,
    api_url: Optional[str] = None,
    config_path: Optional[str] = None,
) -> Client:
    """Get a configured Client.

    Args:
        env: Chain environment
        address: User address
        api_url: Chain API URL
        config_path: Path to configuration file

    Returns:
        Client instance
    """
    return Client(
        env=env,
        user_address=address,
        chain_api_url=api_url,
        config_path=config_path
    )


@app.command("config-info")
def config_info(
    env: Optional[str] = typer.Option(None, "--env", "-e", help="Chain environment"),
    address: Optional[str] = typer.Option(None, "--address", "-a", help="User address"),
    api_url: Optional[str] = typer.Option(None, "--api-url", "-u", help="Chain API URL"),
    config_path: Optional[str] = typer.Option(None, "--config", "-c", help="Path to configuration file"),
):
    """Display current configuration."""
    client = get_client(env, address, api_url, config_path)
    
    console.print("[bold]Current Configuration:[/bold]")
    console.print(f"Environment: [green]{client.config.env}[/green]")
    console.print(f"Chain ID: [green]{client.config.chain_id}[/green]")
    console.print(f"Chain API URL: [green]{client.config.chain_api_url}[/green]")
    console.print(f"User Address: [green]{client.config.user_address or 'Not set'}[/green]")
    console.print(f"Registry Address: [green]{client.config.registry_address or 'Not set'}[/green]")


@app.command("info")
def warp_info(
    tx_hash: str = typer.Argument(..., help="Transaction hash of the Warp"),
    env: Optional[str] = typer.Option(None, "--env", "-e", help="Chain environment"),
    address: Optional[str] = typer.Option(None, "--address", "-a", help="User address"),
    api_url: Optional[str] = typer.Option(None, "--api-url", "-u", help="Chain API URL"),
    config_path: Optional[str] = typer.Option(None, "--config", "-c", help="Path to configuration file"),
):
    """Get information about a Warp."""
    client = get_client(env, address, api_url, config_path)
    
    async def get_info():
        await client.init()
        info = await client.registry.get_warp_info(tx_hash)
        
        if not info:
            console.print(f"[bold red]Warp not found: {tx_hash}[/bold red]")
            return
        
        console.print(f"[bold]Warp Information:[/bold] {tx_hash}")
        console.print(f"Name: [green]{info.get('name', 'Unknown')}[/green]")
        console.print(f"Title: [green]{info.get('title', 'Unknown')}[/green]")
        console.print(f"Description: [green]{info.get('description', 'Unknown')}[/green]")
        
        action = info.get("action", {})
        console.print("[bold]Action:[/bold]")
        console.print(f"Type: [green]{action.get('type', 'Unknown')}[/green]")
        console.print(f"Title: [green]{action.get('title', 'Unknown')}[/green]")
        console.print(f"Description: [green]{action.get('description', 'Unknown')}[/green]")
    
    asyncio.run(get_info())


@app.command("create")
def create_warp(
    name: str = typer.Option(..., "--name", "-n", help="Warp name"),
    title: str = typer.Option(..., "--title", "-t", help="Warp title"),
    description: str = typer.Option(..., "--description", "-d", help="Warp description"),
    action_type: str = typer.Option("transfer", "--action-type", "-a", help="Action type"),
    action_title: str = typer.Option("Transfer", "--action-title", help="Action title"),
    action_description: str = typer.Option("Transfer EGLD", "--action-description", help="Action description"),
    env: Optional[str] = typer.Option(None, "--env", "-e", help="Chain environment"),
    address: Optional[str] = typer.Option(None, "--address", help="User address"),
    api_url: Optional[str] = typer.Option(None, "--api-url", "-u", help="Chain API URL"),
    config_path: Optional[str] = typer.Option(None, "--config", "-c", help="Path to configuration file"),
):
    """Create a simple Warp."""
    client = get_client(env, address, api_url, config_path)
    
    # Build Warp
    warp = client.builder.name(name)\
        .title(title)\
        .description(description)
    
    if action_type == "transfer":
        warp = warp.action_transfer(
            title=action_title,
            description=action_description
        )
    elif action_type == "contract":
        warp = warp.action_contract(
            title=action_title,
            description=action_description
        )
    elif action_type == "query":
        warp = warp.action_query(
            title=action_title,
            description=action_description
        )
    elif action_type == "collect":
        warp = warp.action_collect(
            title=action_title,
            description=action_description
        )
    else:
        console.print(f"[bold red]Invalid action type: {action_type}[/bold red]")
        return
    
    warp = warp.build()
    
    # Create transaction
    tx = client.builder.create_inscription_transaction(warp)
    
    console.print("[bold]Warp Created:[/bold]")
    console.print(f"Name: [green]{warp['name']}[/green]")
    console.print(f"Title: [green]{warp['title']}[/green]")
    console.print(f"Description: [green]{warp['description']}[/green]")
    console.print(f"Action Type: [green]{warp['action']['type']}[/green]")
    
    console.print("\n[bold]Transaction:[/bold]")
    console.print(f"Sender: [green]{tx.sender}[/green]")
    console.print(f"Receiver: [green]{tx.receiver}[/green]")
    console.print(f"Gas Limit: [green]{tx.gas_limit}[/green]")
    console.print(f"Chain ID: [green]{tx.chain_id}[/green]")


@app.command("upgrade")
def upgrade_warp(
    original_tx_hash: str = typer.Argument(..., help="Original transaction hash"),
    new_tx_hash: str = typer.Argument(..., help="New transaction hash"),
    env: Optional[str] = typer.Option(None, "--env", "-e", help="Chain environment"),
    address: Optional[str] = typer.Option(None, "--address", "-a", help="User address"),
    api_url: Optional[str] = typer.Option(None, "--api-url", "-u", help="Chain API URL"),
    config_path: Optional[str] = typer.Option(None, "--config", "-c", help="Path to configuration file"),
):
    """Create an upgrade transaction."""
    client = get_client(env, address, api_url, config_path)
    
    async def upgrade():
        await client.init()
        
        # Create upgrade transaction
        tx = await client.registry.create_warp_upgrade_transaction(
            original_tx_hash=original_tx_hash,
            new_tx_hash=new_tx_hash
        )
        
        console.print("[bold]Upgrade Transaction Created:[/bold]")
        console.print(f"Original TX: [green]{original_tx_hash}[/green]")
        console.print(f"New TX: [green]{new_tx_hash}[/green]")
        console.print(f"Sender: [green]{tx.sender}[/green]")
        console.print(f"Receiver: [green]{tx.receiver}[/green]")
        console.print(f"Gas Limit: [green]{tx.gas_limit}[/green]")
        console.print(f"Chain ID: [green]{tx.chain_id}[/green]")
    
    asyncio.run(upgrade())


if __name__ == "__main__":
    app()
