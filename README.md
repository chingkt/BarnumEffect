# Barnum-Forer Effect
The Barnum effect, also called the Forer effect or, less commonly, the Barnum–Forer effect, is a common psychological phenomenon whereby individuals give high accuracy ratings to descriptions of their personality that supposedly are tailored specifically to them, yet which are in fact vague and general enough to apply to a wide range of people. This effect can provide a partial explanation for the widespread acceptance of some paranormal beliefs and practices, such as astrology, fortune telling, aura reading, and some types of personality tests. (From Wikipedia)

## Technologies

Telegram bot hosting on AWS E2 and RDS using python.

## Goal of this bot
The bot investigates which groups of people in the society are easier to be affected by the Barnum effect.

1. The bot first asks basic background information of the user, e.g. nickname, gender, age, education level etc.
2. The bot lies to the user, claiming to generate a tailor-made discriptions of the user's personality, but in fact the description was specially designed with high-probability guesses.
3. At the end the bot asks user to rate the accuracy of the personality description ranging from 0 to 10.
4. The datapoints are stored in an AWS RDS database for further analysis.
