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
    real mu_offset;
    real<lower=0> sigma_att;
    real<lower=0> sigma_def;
    vector[n_teams] att;
    vector[n_teams] def;
}

model {
    home ~ normal(0.0, 1.0);
    mu_offset ~ normal(0.0, 1.0);
    sigma_att ~ exponential(1.0);
    sigma_def ~ exponential(1.0);
    att ~ normal(0.0, sigma_att);
    def ~ normal(0.0, sigma_def);
    team_1_score ~ poisson_log(mu_offset + att[team_1_id] + def[team_2_id]);
    for (i in 1:n_games) {
        team_2_score[i] ~ poisson_log(
            mu_offset +
            att[team_2_id[i]] +
            def[team_1_id[i]] +
            (home * team_2_home[i])
        );
    }
}

generated quantities {
    int<lower=0> team_1_score_pred[n_games];
    int<lower=0> team_2_score_pred[n_games];
    team_1_score_pred =
        poisson_log_rng(mu_offset + att[team_1_id] + def[team_2_id]);
    for (i in 1:n_games) {
        team_2_score_pred[i] = poisson_log_rng(
            mu_offset +
            att[team_2_id[i]] +
            def[team_1_id[i]] +
            (home * team_2_home[i])
        );
    }
}
