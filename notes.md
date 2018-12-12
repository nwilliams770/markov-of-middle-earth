- Firstly, a Markov process is a **stochastic process** 
    - is a time sequence represnting the evolution of some system represented by a variable whose change is subject to a random variation. 
- A Markov Chain is a sequence of states (or seen as a set of transitions) which can transition between each other with certain probabilities (e.g. determined by some probability distribution that satisfy the Markov property)
- Key feature is they are **memoryless**: the conditional probability distribution of future states of the process ONLY depends on the present state
- We can apply this to text generation! we can model sentences as Markov chains as well, by letting each word be different state
- A Markov Chain has a set of states and some process that can switch these states to one another based on a transition model
- Aren't generally reliable predictors of events in the near term as real-world events more complex than they allow but most useful for examining long-run behavior of a series of events that are related through fixed probabilities
- Let's consider the following example:
    - We can swtich between wearing a white shirt and a blue shirt (our two states)
    - Wearing white shirt: continue wearing white shirt 0.7 and switching to blue is 0.3
    - Wearing blue shirt: continue wearing blue is 0.4 and switching to white is 0.6
    - This can be represented as a transition matrix:
            W     B
        W  0.7   0.3
        B  0.6   0.4
    - And express these transition probabilities as follows: P(W|W) = 0.7, P(B|W) = 0.3, P(W|B) = 0.6, P(B|B) = 0.4
- For our purposes, we would count up every word used, and for every word, the word that was used next. This is the distribution of words in that text CONDITIONAL on the preceding word.
- Because Markov chains are memoryless, they can mimic a writing system based on word frequencies but are unable to produce text that contains deep meaning or thematic significance. They CANNOT produce context-dependent content since they cannot take into account the full chain of prior states
- Probability distribution of state transitions is typically represented as the Markov chain transition matrix:
    - If the chain has N possible states, it will yield an N x N matrix such that entry (I, J) is the probability of transitioning from state I to state J. 
    - This matrix must be a **stochastic matrix**, a matrix whose entries add up to 1 in each row, since each row represents its own probability distribution
    - We also have an **initial state vector**, represented by an N x 1 matrix which describes prob distribution of starting at each of the N possible states. Entry I of the vector describes the probability of each chain starting at state I
    - That's all we need to represent a Markov chain!

- How do we determine the probability of moving from state I to state J over M steps? Apparently it's simple..let's find out!
    - Given a transition matrix P, we can calculate this by calculating the value of entry (I, J) of the matrix obtained raising P to the power of M. 
        - For large values of M, it is more efficient diagnalize the matrix betwen raising it to any power
            - diagnalizing a matrix is long, complex, and cray cray. Involves finding eigenvalues and corresponding eigenvectors

- Let's consider a different example:
    - **corpus**: The data you use to create your model
    - "One fish two fish red fish blue fish"
    - We can view each word as a **token** and each UNIQUE word as a **key**; eight tokens and five keys
    - Our **weighted distribution** for this example is the percentage that one key will appear (based on total key appearances divided by tokens)
    - A **histogram** can be used to represent this weighted distribution, often a plot enables you to discover underlying frequency distribution of a set of continuous data (which in our case ,is a continuous line of text)
    - If we start to look at the frequencies of each key, we can begin to construct a dict that describes the probability that a particular key will appear after another
                START: [One]
                One: [fish]
                fish: [two, red, blue, END]
                two: [fish]
                red: [fish]
                blue: [fish]
                END: [none]
    - Note that we are also using START and END markers (sort of like sentinel nodes). 



- Let's talk about some further topics:
    - Taking into account weighted distributions
        - In any language, some words frequently appear more than others. Knowing how often in comparison one key shows up vs a different key is critical to seeming more realistic
        - We therefore need to take the weighted distribution into account when deciding our next step in the model
        - One way to represent this is to have each key of your dict have a value that is ANOTHER dict, storing the weighted distribution of all possible unique tokens and the amount of their occurences.
        - This is not super different than our previous example because our next step is solely based on the currnet status--but now we can weight the next step as opposed giving each potential word equal weight
    - In previous examples, our "window", that is, our current state, was only one word. We rely upon the ONE word to determine what the next word will be. But what if we INCREASED our window size? Would that allow us to create a more realistic text? 
    - Bigger Windows
        - By using larger windows, we create a more "accurate" text because it will be closer and closer to the original corpus text. To NOTE: a larger window is only a good idea if you have a corpus of 100k+ tokens
            - this is because a smaller data will be unlikely to yield large unique distributions for possible outcomes so we'd just be recreating sentences
        - increasing the size of the window is known as bringing the Markov Model to a **"higher order"**
        - Our previous examples were with **first order markov models**, a second order markov model would have a window of size two
    


- Markov chain Monte Carlo (MCMC) methods:
    - The overview: MCMC methods are used to approximate the posterior distribution of a parameter of interest by random sampling in a probabilistic space.
        - parameter of interest is a number that summarizes a phenemena we are interested in
        - distribution is the mathematical representation of every possible value of our parameter and how likely we are to observe each one. EX: a bell curve
        - 
    - We are working in the context of **Bayesian** approach to stats, and in it, distributions have an additional interpretation. They describe our beliefs about a parameter instead of just the values and the probability each value is the true value
        - This means that there is equal likelihood the true value will be above or below its point on the distribution
    - **prior distribution**: represents our beliefs about a parameter prior to seeing any data
    - **likelihood distribution**: summarizes the observed data, representing range of param values and the likelihood each param explains the data we're observing. 
    - These two are combined to determine the **posterior distribution**: this tells us which param values maximize the chance of observing the particular data we did, taking into account prior beliefs
    - Our dilemma: In the case of two bell curves, there is a simple equation for combining the two to dermine posterior dist, but what about really weird and wacky shaped distributions? MCMC methods allow us to estimate the shape in case we can't compute it directly
    - Let's break it down piece by piece
        - Monte Carlo simulations: a means of estimating a fixed param by repeatedly generating random numbers. By taking random numbers and doing some computation on them, they porvide an approximation of a param where calculating it directly is impossible or very expensive
        - Markov Chains: Sequences of events probabilistically related to any other. Each event comes from a set of outcomes, and each outcome determines which outcome occurs next based on fixed probabilities
            - A famous example was that Markov counted two-char pairs from a work of Russian poetry, using those pairs he computed conditional probability of each char and could simulate a long sequences of chars
            - First few chars largely determined by starting char but Markov showed, in the long run, the distribution of chars settled into a pattern!
            - can be used to compute the **long-run tendency** of a variable if we understand the probabilities that govern its behavior.
    - So, when we can't directly compute posterior dist, we can use MCMC methods to draw samples from the posterior distribution and THEN compute stats like the average on the samples drawn
    - We will pick a random param value to consider. The simulation will generate random values subject to some rule for determining what makes a good param. Then, we can compute which is a better param value but computing how likely each value is to explain the data, GIVEN our prior beliefs.
    - If randomly generated param better, we add to chain of param values with a probability of how much better it is
    - They samples are subject to fixed probabilities and will start to converge in the region of highest probability for the param we're interested in
