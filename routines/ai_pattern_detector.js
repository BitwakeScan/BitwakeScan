class PatternDetector {
  constructor(modelId) {
    this.modelId = modelId;
    this.patterns = [];
    this.recentScores = [];
    this.config = {
      matchThreshold: 0.78,
      decayFactor: 0.95,
      maxPatterns: 50,
    };
  }

  addPattern(signature, metadata) {
    const pattern = {
      id: `pt_${this.patterns.length + 1}`,
      signature,
      metadata,
      createdAt: Date.now(),
    };
    this.patterns.push(pattern);
    if (this.patterns.length > this.config.maxPatterns) {
      this.patterns.shift();
    }
    return pattern;
  }

  scoreMatch(inputVector) {
    if (!inputVector || inputVector.length === 0) return 0;
    let maxScore = 0;
    for (const p of this.patterns) {
      const sim = this.cosineSimilarity(inputVector, p.signature);
      maxScore = Math.max(maxScore, sim);
    }
    this.recentScores.push(maxScore);
    return maxScore;
  }

  cosineSimilarity(a, b) {
    const dot = a.reduce((sum, val, i) => sum + val * b[i], 0);
    const magA = Math.sqrt(a.reduce((sum, val) => sum + val * val, 0));
    const magB = Math.sqrt(b.reduce((sum, val) => sum + val * val, 0));
    return magA && magB ? dot / (magA * magB) : 0;
  }

  detect(inputVector) {
    const score = this.scoreMatch(inputVector);
    return score >= this.config.matchThreshold;
  }

  recentAverage() {
    if (this.recentScores.length === 0) return 0;
    const sum = this.recentScores.reduce((a, b) => a + b, 0);
    return sum / this.recentScores.length;
  }

  decayHistory() {
    this.recentScores = this.recentScores.map(s => s * this.config.decayFactor);
  }

  explainTopMatches(inputVector, topN = 3) {
    const scored = this.patterns.map(p => ({
      id: p.id,
      score: this.cosineSimilarity(inputVector, p.signature),
    }));
    return scored.sort((a, b) => b.score - a.score).slice(0, topN);
  }

  adjustThreshold(newThreshold) {
    this.config.matchThreshold = newThreshold;
  }

  dumpSummary() {
    return {
      model: this.modelId,
      patternsStored: this.patterns.length,
      recentAvgScore: this.recentAverage(),
    };
  }
}

function generateRandomVector(length = 16) {
  return Array.from({ length }, () => parseFloat((Math.random() * 2 - 1).toFixed(4)));
}

function generateRandomMetadata() {
  return {
    origin: Math.random() > 0.5 ? "live" : "historical",
    riskLevel: ["low", "medium", "high"][Math.floor(Math.random() * 3)],
    createdBy: `system_${Math.floor(Math.random() * 10)}`,
  };
}

const detector = new PatternDetector("ai-risk-engine-v2");

for (let i = 0; i < 30; i++) {
  detector.addPattern(generateRandomVector(), generateRandomMetadata());
}

const inputSamples = Array.from({ length: 10 }, () => generateRandomVector());

const matchResults = inputSamples.map((vec, idx) => {
  const isMatch = detector.detect(vec);
  const explanation = detector.explainTopMatches(vec, 2);
  return {
    sample: idx,
    matched: isMatch,
    explanation,
  };
});

const thresholds = [0.5, 0.6, 0.7, 0.8, 0.9];
const responses = thresholds.map(thresh => {
  detector.adjustThreshold(thresh);
  const rate = inputSamples.filter(vec => detector.detect(vec)).length / inputSamples.length;
  return { threshold: thresh, detectionRate: rate };
});

console.log("Detection Results:");
console.table(matchResults);

console.log("Threshold Responses:");
console.table(responses);

console.log("Summary:");
console.log(detector.dumpSummary());