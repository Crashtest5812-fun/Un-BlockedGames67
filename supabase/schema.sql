create table if not exists public.game_ratings (
    game_id text not null check (char_length(game_id) between 1 and 300),
    user_id uuid not null references auth.users (id) on delete cascade,
    rating smallint not null check (rating between 1 and 5),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    primary key (game_id, user_id)
);

alter table public.game_ratings enable row level security;

drop policy if exists "Users can read their own game ratings" on public.game_ratings;
create policy "Users can read their own game ratings"
    on public.game_ratings
    for select
    to authenticated
    using ((select auth.uid()) = user_id);

drop policy if exists "Users can create their own game ratings" on public.game_ratings;
create policy "Users can create their own game ratings"
    on public.game_ratings
    for insert
    to authenticated
    with check ((select auth.uid()) = user_id);

drop policy if exists "Users can update their own game ratings" on public.game_ratings;
create policy "Users can update their own game ratings"
    on public.game_ratings
    for update
    to authenticated
    using ((select auth.uid()) = user_id)
    with check ((select auth.uid()) = user_id);

drop policy if exists "Users can delete their own game ratings" on public.game_ratings;
create policy "Users can delete their own game ratings"
    on public.game_ratings
    for delete
    to authenticated
    using ((select auth.uid()) = user_id);

revoke all on table public.game_ratings from anon, authenticated;
grant select, insert, update, delete on table public.game_ratings to authenticated;

create or replace function public.set_game_rating_updated_at()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
    new.updated_at = now();
    return new;
end;
$$;

drop trigger if exists set_game_rating_updated_at on public.game_ratings;
create trigger set_game_rating_updated_at
    before update on public.game_ratings
    for each row
    execute function public.set_game_rating_updated_at();

create or replace view public.game_rating_summary
with (security_invoker = false)
as
select
    game_id,
    round(avg(rating)::numeric, 2) as average_rating,
    count(*)::integer as rating_count
from public.game_ratings
group by game_id;

revoke all on table public.game_rating_summary from public, anon, authenticated;
grant select on table public.game_rating_summary to anon, authenticated;
