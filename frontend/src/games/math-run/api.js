import apiClient from '@/api/client'

export const submitMathRunScore = (score, category) =>
  apiClient
    .post('/api/mini-games/math-run/score/', { score, category })
    .catch(() => null)  // silent — never block game flow

export const getMathRunLeaderboard = (category = 'all', limit = 10) =>
  apiClient
    .get('/api/mini-games/math-run/leaderboard/', { params: { category, limit } })
    .catch(() => null)
