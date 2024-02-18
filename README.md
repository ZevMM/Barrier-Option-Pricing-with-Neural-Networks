# Barrier-Option-Pricing-with-Neural-Networks
This is my project for the Columbia Data Science Society Fellowship

Exotic options are difficult to price because there are no equations to directly solve for a fair price, and pricing based on the market is difficult due to low trading volume. 
THe traditional approach is to calculate a price based on simulations of the underlier, but calibrating these simulations of the underlier to be consistent with the market is an imprecise and time-consuming process.
The approach I took was to run Monte Carlo simulations of undeliers with many different parameters, and calculate the value of both an exotic option and a European option in every case. 
I then used my pairings of European and exotic option prices to train a neural net mapping between the two.
(This description is unfinished)
