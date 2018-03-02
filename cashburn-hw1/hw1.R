yelp <- read.csv(file="yelp.csv", header = TRUE, quote = "\"", comment.char = "")
names(yelp)

summary(yelp)
summary(yelp$noiseLevel)
summary(yelp$stars)

jpeg('foo.jpg')
hist(yelp$checkins, main = "Frequency of Check-Ins")
dev.off()

hist(log(yelp$checkins), main = "Logged Frequency of Check-Ins")

#Part 5
yelp <- cbind(yelp, isAmerican=grepl("American", yelp$categories), goodForDinner=grepl("dinner", yelp$recommendedFor))
summary(yelp$isAmerican)
summary(yelp$goodForDinner)

print("Review Count Original/Modified", quotes = FALSE)
quantile(yelp$reviewCount)
quantile(yelp$reviewCount[yelp$reviewCount <= quantile(yelp$reviewCount)[2]])

summary(yelp$reviewCount[yelp$reviewCount <= quantile(yelp$reviewCount)[2]])
summary(yelp$stars[yelp$reviewCount <= quantile(yelp$reviewCount)[2]])
summary(yelp$attire[yelp$reviewCount <= quantile(yelp$reviewCount)[2]])
summary(yelp$priceRange[yelp$reviewCount <= quantile(yelp$reviewCount)[2]])
summary(yelp$delivery[yelp$reviewCount <= quantile(yelp$reviewCount)[2]])
summary(yelp$goodForKids[yelp$reviewCount <= quantile(yelp$reviewCount)[2]])

#Part 6
pairs(~stars+reviewCount+checkins+longitude+latitude, data=yelp)


