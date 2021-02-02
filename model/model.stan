data {
    int<lower=1> n_games;
    int<lower=1> n_teams;
    int<lower=1> team_1_id[n_games];
    int<lower=1> team_2_id[n_games];
    int<lower=0> team_1_score[n_games];
    int<lower=0> team_2_score[n_games];
    int<lower=0, upper=1> team_2_home[n_games];
}

parameters {
    real home;
    real<lower=0> sigma_att;
    real<lower=0> sigma_def;
    vector[n_teams] att;
    vector[n_teams] def;
}

model {
    home ~ normal(0.0, 0.1);
    sigma_att ~ exponential(4.0);
    sigma_def ~ exponential(4.0);
    att ~ normal(0.0, sigma_att);
    def ~ normal(0.0, sigma_def);
    team_1_score ~ poisson_log(att[team_1_id] + def[team_2_id]);
    for (i in 1:n_games) {
        team_2_score[i] ~ poisson_log(
            (home * team_2_home[i]) + att[team_2_id[i]] + def[team_1_id[i]]
        );
    }
}
