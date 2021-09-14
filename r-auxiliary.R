# 

url <- './PycharmProjects/corona_map/data/owid_all.csv'


url <- '../Pycharm_projects/corona_maps/data/owid_all.csv'


df <- read.csv(url)

colnames(df)

cols <- colnames(df)[grep('test|popul', colnames(df))]
cols

dfx <- df[, cols]

rowSums(is.na(dfx))

dfx[2,]



cols <- c(2, 6, 12, 48)

dfx <- df[100, cols]

dfx

dfx$total_cases / dfx$population * 1e+6



x <- dfx$total_tests / dfx$population * 1e+3
y <- dfx$total_tests_per_thousand

ind <- is.na(x) & is.na(y)

x <- x[!ind]
y <- y[!ind]

ind <- abs(x - y) > 0.0001

View(cbind(x, y)[ind,])


