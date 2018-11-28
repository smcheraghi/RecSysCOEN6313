# ATRank recommendation API

## Dependencies
Python >= 3.6.1
NumPy >= 1.12.1
TensorFlow >= 1.4.0 (Probably earlier version should work too, though I didn't test it)

## Usage
Input: A list of dict contains following information:
[{reviewerID, asin, unixReviewtime}, {reviewerID, asin, unixReviewtime}]
Note the reviewerID should be the same

Output:
The asin number list. Which reviewer may take action on. ranked by probability from high to low.



