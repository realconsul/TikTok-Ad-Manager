create table if not exists public.video_analytics (
    id bigint generated always as identity primary key,
    video_id text not null,
    caption text,
    posting_time timestamptz not null,
    views bigint default 0,
    likes bigint default 0,
    comments bigint default 0,
    shares bigint default 0,
    saves bigint default 0,
    watch_time double precision default 0,
    completion_rate double precision default 0,
    follower_growth_after_post bigint default 0,
    video_length_seconds integer default 0,
    inserted_at timestamptz default now(),
    unique(video_id, posting_time)
);
