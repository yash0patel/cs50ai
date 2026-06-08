# Analysis

## Layer 3, Head 10

This attention head seems to focus mostly on the current word itself. In the attention diagram, the brightest squares appear mainly along the diagonal, which means each token is giving a high amount of attention to itself. This could help BERT keep track of the meaning of individual words while processing the sentence.

Example Sentences:

I drink [MASK] every morning.
The cat chased a [MASK].

## Layer 4, Head 11

This attention head appears to focus on important words near the end of the sentence, especially around the `[SEP]` token. Several tokens give noticeable attention to these positions, suggesting that this head may help BERT understand the overall sentence structure and context before predicting the masked word.

Example Sentences:

I drink [MASK] every morning.
The cat chased a [MASK].