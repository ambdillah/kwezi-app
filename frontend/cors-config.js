// Configuration CORS pour Expo afin de permettre les requêtes depuis Emergent
module.exports = {
  // Origines autorisées pour les requêtes CORS
  allowedOrigins: [
    'https://app.emergent.sh',
    'https://emergent.sh',
    'https://kwezi-linguist.preview.emergentagent.com',
    'http://localhost:3000',
    'http://localhost:19006',
  ],
  // Headers autorisés
  allowedHeaders: [
    'Content-Type',
    'Authorization',
    'X-Requested-With',
    'Accept',
    'Origin',
  ],
  // Méthodes autorisées
  allowedMethods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'],
  // Permettre les credentials
  credentials: true,
};
