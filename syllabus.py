"""
syllabus.py

Official CMDA syllabus definition.
The AI agent MUST restrict teaching, explanations,
and problem solving strictly to the topics listed here.
University: MIT World Peace University (MIT-WPU), Pune
Subject: CMDA
"""

CMDA_SYLLABUS = {
    "Unit 1: Introduction": [
        "Basic concepts of Statistics",
        "Measures of central tendency (Mean, Median, Mode)",
        "Relative frequency",
        "Class frequency tables",
        "Frequency histogram",
        "Basics of Probability",
        "Complementary events",
        "Independent events",
        "Conditional probability",
        "Bayesian Inference",
        "Frequentist vs Bayesian approach",
        "Bayes Theorem",
        "Measures of Variation: Quartiles",
        "Measures of Variation: Percentiles",
        "Moments: Skewness",
        "Moments: Kurtosis",
        "Correlation"
    ],

    "Unit 2: Random Variables and Probability Distributions": [
        "Definition of Random Variable",
        "Discrete Random Variables",
        "Continuous Random Variables",
        "Distribution Function of a Random Variable",
        "Probability Mass Function (PMF)",
        "Probability Density Function (PDF)",
        "Binomial Distribution",
        "Poisson Distribution",
        "Geometric Distribution",
        "Uniform Distribution",
        "Normal Distribution",
        "Exponential Distribution"
    ],

    "Unit 3: Sampling Distribution and Estimation": [
        "Sampling Theory",
        "Random Sampling",
        "Stratified Sampling",
        "Systematic Sampling",
        "Central Limit Theorem",
        "Point Estimation",
        "Interval Estimation"
    ],

    "Unit 4: Hypothesis Testing": [
        "Null Hypothesis",
        "Alternative Hypothesis",
        "Type I Error",
        "Type II Error",
        "Level of Significance",
        "p-value",
        "Z-test (One Sample)",
        "Z-test (Two Sample)",
        "t-test (One Sample)",
        "t-test (Two Sample)",
        "Paired t-test"
    ],

    "Unit 5: Regression": [
        "Simple Linear Regression",
        "Regression Model",
        "Regression Equation",
        "Least Square Method",
        "Testing for Significance of Regression",
        "Residual Analysis"
    ]
}


def is_topic_in_syllabus(topic: str) -> bool:
    """
    Checks whether a given topic belongs to the CMDA syllabus.
    Prevents the agent from answering out-of-syllabus questions.
    """
    topic = topic.lower()
    for unit_topics in CMDA_SYLLABUS.values():
        for t in unit_topics:
            if topic in t.lower():
                return True
    return False
