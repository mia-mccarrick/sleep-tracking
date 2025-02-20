library(ggplot2)
library(dplyr)
library(lubridate)
library(tidyverse)

# Read and prepare data
sleep_data <- read.csv("sleep classified.csv")
sleep_data <- sleep_data %>% filter(state != "neither")

sleep_data$row_id <- rep(1:(nrow(sleep_data) / 2), each = 2)

night_data <- sleep_data %>%
  group_by(row_id) %>%
  summarize(
    sleep_time = first(end_time), 
    wake_up_time = last(start_time), 
    sleep_duration = last(time_gap)  
  ) %>%
  select(sleep_time, wake_up_time, sleep_duration)

night_data <- night_data %>%
  mutate(day_of_week = rep(c("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"), length.out = nrow(night_data)))

night_data <- night_data %>%
  mutate(
    sleep_time = ymd_hms(sleep_time),  
    wake_up_time = ymd_hms(wake_up_time)  
)

night_data <- night_data %>%
  mutate(day_type = ifelse((day_of_week == "Sat" | day_of_week == "Sun"), "Weekend", "Weekday"))


initial_reference_time <- ymd_hms("2025-01-12 20:00:00")

night_data <- night_data %>%
  mutate(
    reference_time = initial_reference_time + days(row_number() - 1),
    sleep_time_relative = as.numeric(difftime(sleep_time, reference_time, units = "mins")),
    wake_up_time_relative = as.numeric(difftime(wake_up_time, reference_time, units = "mins"))
  )

night_data_long <- night_data %>%
  gather(key = "time_type", value = "time_relative", sleep_time_relative, wake_up_time_relative)

#Visualization 1: Histogram to show sleep duration distribution
ggplot(night_data, aes(x = sleep_duration, fill = day_type)) +
  geom_histogram(binwidth = 1, color = "black", alpha = 1) +
  scale_fill_manual(values = c("Weekend" = "#4e9651", "Weekday" = "#0d82c5")) +
  guides(fill = guide_legend(title = "Type of Day")) + 
  labs(
    title = "Distribution of Sleep Duration",
    x = "Sleep Duration (Hours)",
    y = "Frequency (Days)"
  ) + 
  theme(plot.title = element_text(hjust = 0.5, size = 16, face = "bold")) 
  theme_minimal()

#Visualization 2: Box Plot to show sleep/wake time distribution
  ggplot(night_data_long, aes(x = day_of_week, y = time_relative, fill = time_type)) +
    geom_boxplot(alpha = 0.8) +
    labs(
      title = "Sleep Time and Wake Up Time Distribution",
      x = "Day of the Week",
      y = "Time"
    ) +
    scale_fill_manual(values = c("sleep_time_relative" = "#2a4982", "wake_up_time_relative" = "#f5d30f"),
                      labels = c("Fall Asleep Time", "Wake Up Time")) +
    scale_y_continuous(
      breaks = seq(0, 960, by = 60),  # Set breaks at every 60 minutes (1 hour)
      labels = c("8:00PM", "9:00PM", "10:00PM", "11:00PM", "12:00AM", "1:00AM", "2:00AM", "3:00AM",
                 "4:00AM", "5:00AM", "6:00AM", "7:00AM", "8:00AM", "9:00AM", "10:00AM", "11:00AM", "12:00PM")
    ) +
    theme_minimal() +
    theme(
      plot.title = element_text(hjust = 0.5, size = 16, face = "bold"),
      axis.text.x = element_text(angle = 45, hjust = 1),
      legend.title = element_blank(),  # Remove legend title
      legend.position = "top"
    )