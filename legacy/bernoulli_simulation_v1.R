# ==================================================
# Coin Toss Simulation
# Author: Muhammad İkbal Yılmaz
# github: https://github.com/mikbalyilmaz
# ==================================================

# Set seed for reproducibility
set.seed(42)

# -----------------------------
# Parameters
# -----------------------------
p_success  <- 0.5677     # Probability of success (for Bernoulli trial)
num_trials <- 1000       # Number of simulations
# num_trials <- 1e6      # Alternative notation (scientific)

# -----------------------------
# 1. Bernoulli Trial
# -----------------------------
bernoulli_result <- rbinom(1, size = 1, prob = p_success)
cat("Single Bernoulli trial result:", bernoulli_result, "\n\n")

# -----------------------------
# 2. Simulate Coin Tosses
# -----------------------------
results <- sample(c("Heads", "Tails"),
                  size    = num_trials,
                  replace = TRUE)

# -----------------------------
# 3. Frequency and Proportion
# -----------------------------
freq_table <- table(results)
proportions <- prop.table(freq_table)

cat("Frequencies:\n")
print(freq_table)

cat("\nProportions:\n")
print(round(proportions, 4))

# -----------------------------
# 4. Visualizations
# -----------------------------

# 4.1 Bar Plot: Frequency Distribution
barplot(freq_table,
        col  = c("steelblue", "tomato"),
        main = "Coin Toss - Frequency Distribution",
        ylab = "Frequency",
        xlab = "Outcome")

# 4.2 Cumulative Probability Plot
cumulative <- cumsum(ifelse(results == "Heads", 1, 0)) / seq_along(results)

plot(cumulative, type = "l", col = "darkgreen",
     main = "Cumulative Probability (Heads)",
     xlab = "Number of Tosses",
     ylab = "Proportion")

# Theoretical probability line
abline(h = 0.5, col = "red", lty = 2)
