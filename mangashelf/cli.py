import os
from datetime import datetime
from typing import List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm, FloatPrompt
from rich import print as rprint
from .models import Manga
from .storage import save_manga_list, load_manga_list

console = Console()

STATUS_OPTIONS = ["Reading", "Completed", "On Hold", "Dropped", "Plan to Read"]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    console.print(Panel.fit(
        "[bold cyan]MangaShelf Tracker[/bold cyan]\n"
        "[dim]Your personal manga library manager[/dim]",
        border_style="magenta"
    ))
    rprint("[1] 📚 View Manga List")
    rprint("[2] ➕ Add New Manga")
    rprint("[3] 🆙 Update Progress")
    rprint("[4] 🔄 Change Status")
    rprint("[5] ⭐ Rate/Review")
    rprint("[6] 🔍 Search Manga")
    rprint("[7] 📊 View Statistics")
    rprint("[8] ❌ Remove Manga")
    rprint("[0] 🚪 Exit")
    rprint("")

def list_manga(manga_list: List[Manga], sort_by: str = "title"):
    if not manga_list:
        rprint("[yellow]Your shelf is empty! Add some manga first.[/yellow]")
        return

    # Sorting
    if sort_by == "title":
        manga_list.sort(key=lambda x: x.title.lower())
    elif sort_by == "rating":
        manga_list.sort(key=lambda x: x.rating if x.rating is not None else -1, reverse=True)
    elif sort_by == "updated":
        manga_list.sort(key=lambda x: x.last_updated, reverse=True)

    table = Table(title="Your Manga Shelf", border_style="cyan")
    table.add_column("No.", justify="right", style="dim")
    table.add_column("Title", style="bold white")
    table.add_column("Author", style="green")
    table.add_column("Progress", justify="center")
    table.add_column("Status", justify="center")
    table.add_column("Rating", justify="center")
    table.add_column("Last Updated", style="dim")

    for i, manga in enumerate(manga_list, 1):
        progress = f"{manga.current_chapter}/{manga.total_chapters if manga.total_chapters else '?'}"
        status_color = {
            "Reading": "blue",
            "Completed": "green",
            "On Hold": "yellow",
            "Dropped": "red",
            "Plan to Read": "magenta"
        }.get(manga.status, "white")
        
        rating_str = f"⭐ {manga.rating:.1f}" if manga.rating is not None else "N/A"
        updated_date = datetime.fromisoformat(manga.last_updated).strftime("%Y-%m-%d %H:%M")

        table.add_row(
            str(i),
            manga.title,
            manga.author,
            progress,
            f"[{status_color}]{manga.status}[/{status_color}]",
            rating_str,
            updated_date
        )

    console.print(table)

def add_manga(manga_list: List[Manga]):
    rprint("\n[bold green]Add New Manga[/bold green]")
    title = Prompt.ask("Title")
    author = Prompt.ask("Author")
    
    total_chapters_input = Prompt.ask("Total Chapters (Press Enter if unknown)", default="")
    total_chapters = int(total_chapters_input) if total_chapters_input.isdigit() else None
    
    current_chapter = IntPrompt.ask("Current Chapter", default=0)
    
    rprint("\nSelect Status:")
    for i, status in enumerate(STATUS_OPTIONS, 1):
        rprint(f"[{i}] {status}")
    status_idx = IntPrompt.ask("Choose status", choices=[str(i) for i in range(1, len(STATUS_OPTIONS)+1)], default=5)
    status = STATUS_OPTIONS[int(status_idx) - 1]
    
    notes = Prompt.ask("Initial Notes (Optional)", default="")
    
    new_manga = Manga(
        title=title, 
        author=author, 
        current_chapter=current_chapter, 
        total_chapters=total_chapters,
        status=status,
        notes=notes
    )
    manga_list.append(new_manga)
    save_manga_list(manga_list)
    rprint(f"\n[green]Successfully added '{title}' to your shelf![/green]")

def update_progress(manga_list: List[Manga]):
    list_manga(manga_list)
    if not manga_list: return
    
    idx = IntPrompt.ask("\nEnter the Number of the manga to update") - 1
    if 0 <= idx < len(manga_list):
        manga = manga_list[idx]
        new_chapter = IntPrompt.ask(f"Updating '{manga.title}'. Current chapter: {manga.current_chapter}. New current chapter")
        manga.current_chapter = new_chapter
        manga.last_updated = datetime.now().isoformat()
        
        if manga.total_chapters and manga.current_chapter >= manga.total_chapters:
            if Confirm.ask("You've reached or passed the total chapters. Mark as Completed?"):
                manga.status = "Completed"
        
        save_manga_list(manga_list)
        rprint("[green]Progress updated![/green]")
    else:
        rprint("[red]Invalid selection.[/red]")

def change_status(manga_list: List[Manga]):
    list_manga(manga_list)
    if not manga_list: return
    
    idx = IntPrompt.ask("\nEnter the Number of the manga to change status") - 1
    if 0 <= idx < len(manga_list):
        manga = manga_list[idx]
        rprint(f"\nCurrent status of '{manga.title}': [bold]{manga.status}[/bold]")
        for i, status in enumerate(STATUS_OPTIONS, 1):
            rprint(f"[{i}] {status}")
        status_idx = IntPrompt.ask("Choose new status", choices=[str(i) for i in range(1, len(STATUS_OPTIONS)+1)])
        manga.status = STATUS_OPTIONS[int(status_idx) - 1]
        manga.last_updated = datetime.now().isoformat()
        save_manga_list(manga_list)
        rprint(f"[green]Status changed to {manga.status}[/green]")
    else:
        rprint("[red]Invalid selection.[/red]")

def rate_review(manga_list: List[Manga]):
    list_manga(manga_list)
    if not manga_list: return
    
    idx = IntPrompt.ask("\nEnter the Number of the manga to rate/review") - 1
    if 0 <= idx < len(manga_list):
        manga = manga_list[idx]
        rprint(f"\n[bold]{manga.title}[/bold]")
        rating = FloatPrompt.ask("Personal Rating (0-10)", default=manga.rating if manga.rating else 0.0)
        manga.rating = max(0.0, min(10.0, rating))
        
        rprint(f"Current Notes: {manga.notes if manga.notes else 'None'}")
        new_notes = Prompt.ask("New Notes (Press Enter to keep current)", default=manga.notes)
        manga.notes = new_notes
        
        manga.last_updated = datetime.now().isoformat()
        save_manga_list(manga_list)
        rprint("[green]Rating and notes updated![/green]")
    else:
        rprint("[red]Invalid selection.[/red]")

def search_manga(manga_list: List[Manga]):
    query = Prompt.ask("\nSearch by Title, Author, or Status").lower()
    results = [
        m for m in manga_list 
        if query in m.title.lower() or query in m.author.lower() or query in m.status.lower()
    ]
    if results:
        list_manga(results)
    else:
        rprint(f"[yellow]No results found for '{query}'[/yellow]")

def view_stats(manga_list: List[Manga]):
    if not manga_list:
        rprint("[yellow]No data to show stats for.[/yellow]")
        return
    
    total = len(manga_list)
    ratings = [m.rating for m in manga_list if m.rating is not None]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0
    
    status_counts = {}
    for status in STATUS_OPTIONS:
        status_counts[status] = sum(1 for m in manga_list if m.status == status)
    
    stats_panel = Panel(
        f"[bold cyan]Statistics[/bold cyan]\n\n"
        f"Total Manga: [bold]{total}[/bold]\n"
        f"Average Rating: [bold yellow]{avg_rating:.2f}/10[/bold yellow]\n\n"
        + "\n".join([f"{status}: {count}" for status, count in status_counts.items()]),
        border_style="green"
    )
    console.print(stats_panel)
    Prompt.ask("\nPress Enter to return to menu")

def remove_manga(manga_list: List[Manga]):
    list_manga(manga_list)
    if not manga_list: return
    
    idx = IntPrompt.ask("\nEnter the Number of the manga to REMOVE") - 1
    if 0 <= idx < len(manga_list):
        manga = manga_list[idx]
        if Confirm.ask(f"[red]Are you sure you want to remove '{manga.title}'?[/red]"):
            manga_list.pop(idx)
            save_manga_list(manga_list)
            rprint("[green]Manga removed from shelf.[/green]")
    else:
        rprint("[red]Invalid selection.[/red]")

def main_loop():
    manga_list = load_manga_list()
    
    while True:
        clear_screen()
        display_menu()
        choice = Prompt.ask("Select an option", choices=[str(i) for i in range(9)])
        
        if choice == "1":
            clear_screen()
            rprint("[bold cyan]Viewing Manga Shelf[/bold cyan]")
            sort_choice = Prompt.ask("Sort by", choices=["title", "rating", "updated"], default="title")
            list_manga(manga_list, sort_by=sort_choice)
            Prompt.ask("\nPress Enter to return to menu")
        elif choice == "2":
            add_manga(manga_list)
            Prompt.ask("\nPress Enter to return to menu")
        elif choice == "3":
            update_progress(manga_list)
            Prompt.ask("\nPress Enter to return to menu")
        elif choice == "4":
            change_status(manga_list)
            Prompt.ask("\nPress Enter to return to menu")
        elif choice == "5":
            rate_review(manga_list)
            Prompt.ask("\nPress Enter to return to menu")
        elif choice == "6":
            search_manga(manga_list)
            Prompt.ask("\nPress Enter to return to menu")
        elif choice == "7":
            view_stats(manga_list)
        elif choice == "8":
            remove_manga(manga_list)
            Prompt.ask("\nPress Enter to return to menu")
        elif choice == "0":
            rprint("[bold blue]Goodbye! Happy reading![/bold blue]")
            break
