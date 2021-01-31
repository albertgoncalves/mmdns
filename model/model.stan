data {
    int<lower=0> n_games;
    int<lower=0> n_teams;
    int<lower=0> team_1_id[n_games];
    int<lower=0> team_2_id[n_games];
    int<lower=0> team_1_score[n_games];
    int<lower=0> team_2_score[n_games];
    int<lower=0> team_2_home[n_games];
}

parameters {
    real home;
    vector[n_teams] att;
    vector[n_teams] def;

    real mu_att;
    real mu_def;
    real<lower=0> tau_att;
    real<lower=0> tau_def;
}

model {
    vector[n_games] theta_1;
    vector[n_games] theta_2;

    home ~ normal(0.0, 0.01);

    mu_att ~ normal(0.0, 0.1);
    mu_def ~ normal(0.0, 0.1);

    tau_att ~ cauchy(0.0, 1.0);
    tau_def ~ cauchy(0.0, 1.0);

    att ~ normal(mu_att, tau_att);
    def ~ normal(mu_def, tau_def);

    theta_1 = att[team_1_id] - def[team_2_id];
    for (i in 1:n_games) {
        theta_2[i] =
            ((home * team_2_home[i]) + att[team_2_id[i]]) - def[team_1_id[i]];
    }

    team_1_score ~ poisson_log(theta_1);
    team_2_score ~ poisson_log(theta_2);
}
