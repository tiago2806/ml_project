const fs = require('fs');
const path = require('path');

const overviewPath = path.join(__dirname, '../../public/data/dataset_overview.json');
const clustersPath = path.join(__dirname, '../../public/data/clusters.json');

const overview = JSON.parse(fs.readFileSync(overviewPath, 'utf8'));
const clusters = JSON.parse(fs.readFileSync(clustersPath, 'utf8'));

const globalStats = overview.numeric_stats;
const clusterData = clusters;

const FEATURES = {
  'sim-age': 'customer_age',
  'sim-children': 'total_children',
  'sim-tenure': 'years_tenure',
  'sim-promo': 'percentage_of_products_bought_promotion',
  'sim-meat': 'lifetime_spend_meat_fish',
  'sim-tech': 'lifetime_spend_electronics_videogames',
  'sim-veg': 'lifetime_spend_vegetables',
  'sim-hyg': 'lifetime_spend_hygiene',
  'sim-stores': 'distinct_stores_visited',
  'sim-complaints': 'number_complaints'
};

// Simulate input values
const inputValues = {
  'customer_age': 45,
  'total_children': 1,
  'years_tenure': 5,
  'percentage_of_products_bought_promotion': 20 / 100,
  'lifetime_spend_meat_fish': 300,
  'lifetime_spend_electronics_videogames': 500,
  'lifetime_spend_vegetables': 100,
  'lifetime_spend_hygiene': 100,
  'distinct_stores_visited': 3,
  'number_complaints': 0
};

// 2. Standardize inputs
const standardizedInput = {};
Object.entries(inputValues).forEach(([feature, val]) => {
  const mean = globalStats[feature] ? globalStats[feature].mean : 0;
  const std = globalStats[feature] ? globalStats[feature].std : 1;
  standardizedInput[feature] = std > 0 ? (val - mean) / std : 0;
});

// 3. Calculate distance
let bestClusterId = null;
let minDistance = Infinity;

Object.values(clusterData).forEach(cluster => {
  let distanceSq = 0;

  Object.keys(cluster.features).forEach(feature => {
    const clusterMean = cluster.features[feature] || 0;
    const globalMean = globalStats[feature] ? globalStats[feature].mean : 0;
    const std = globalStats[feature] ? globalStats[feature].std : 1;

    const standardizedClusterVal = std > 0 ? (clusterMean - globalMean) / std : 0;
    const userVal = standardizedInput[feature] !== undefined ? standardizedInput[feature] : 0;

    const diff = userVal - standardizedClusterVal;
    const weight = standardizedInput[feature] !== undefined ? 2.0 : 1.0;

    distanceSq += (diff * diff) * weight;
  });

  const distance = Math.sqrt(distanceSq);
  console.log(`Distance to cluster ${cluster.id}: ${distance}`);
  if (distance < minDistance) {
    minDistance = distance;
    bestClusterId = cluster.id;
  }
});

const matchScore = Math.max(0, Math.min(100, Math.round(100 - (minDistance * 12))));
console.log(`Best cluster: ${bestClusterId}, Score: ${matchScore}`);
