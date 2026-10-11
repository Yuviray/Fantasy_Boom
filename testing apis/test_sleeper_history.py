from espn_api.football import League

league_id = 193562812

league = League(
    league_id=league_id,
    year=2026
)

for team in league.teams:
    print(team.team_name)

print("\nPlayers:")

for player in league.teams[0].roster:
    print(
        player.name,
        player.position,
        player.stats
    )