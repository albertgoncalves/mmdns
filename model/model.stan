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
    real mu_att;
    real mu_def;
    real<lower=0> sigma_att;
    real<lower=0> sigma_def;
    vector[n_teams] att;
    vector[n_teams] def;
}

model {
    home ~ normal(0.0, 0.01);
    mu_att ~ normal(0.0, 0.01);
    mu_def ~ normal(0.0, 0.01);
    sigma_att ~ normal(0.0, 0.1);
    sigma_def ~ normal(0.0, 0.1);
    att ~ normal(mu_att, sigma_att);
    def ~ normal(mu_def, sigma_def);
    team_1_score ~ poisson_log(att[team_1_id] + def[team_2_id]);
    for (i in 1:n_games) {
        team_2_score[i] ~ poisson_log(
            (home * team_2_home[i]) + att[team_2_id[i]] + def[team_1_id[i]]
        );
    }
}

generated quantities {
    int<lower=0> team_1_score_pred[n_games];
    int<lower=0> team_2_score_pred[n_games];
    team_1_score_pred = poisson_log_rng(att[team_1_id] + def[team_2_id]);
    for (i in 1:n_games) {
        team_2_score_pred[i] = poisson_log_rng(
            (home * team_2_home[i]) + att[team_2_id[i]] + def[team_1_id[i]]
        );
    }
}
