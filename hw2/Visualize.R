library(RColorBrewer)
setwd("~/Documents/cs373/hw2")
allColors = as.vector(cbind(brewer.pal(8, "Set2"), brewer.pal(12, "Set3"), brewer.pal(9, "Pastel1"), brewer.pal(8, "Pastel2"), brewer.pal(12, "Paired"), brewer.pal(8, "Accent")))
yelp <- read.csv(file="yelp.csv", header = TRUE, quote = "\"", comment.char = "")
yelp2 <- yelp[,c("latitude", "longitude", "reviewCount", "checkins")]
points <- read.csv(file="points.csv", header = TRUE, quote = "\"", comment.char = "")
dummy <- read.csv(file="dummy.csv", header = TRUE, quote = "\"", comment.char = "")
centroids <- read.csv(file="centroids.csv", header = TRUE, quote = "\"", comment.char = "")

cluster <- kmeans(yelp2, 32, 20)

plot(yelp2$reviewCount, yelp2$checkins, col=allColors[cluster$cluster])
#plot(yelp2$reviewCount, yelp2$checkins, col=allColors[points$cluster + 1])
#points(centroids$reviewCount, centroids$checkins, col="black", pch=17)

