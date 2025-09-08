import apiClient from './client'

/**
 * Register a new user.
 * Expects: { first_name, last_name, email, password, ... }
 * Adjust keys according to your Django serializer.
 */
export const registerUser = (payload) => apiClient.post('/api/users/register/', payload)

// Map RegisterModal form fields to backend serializer keys
export const mapRegisterFormToPayload = (data) => ({
  first_name: data.firstName,
  last_name: data.lastName,
  email: data.email,
  password: data.password,
  password2: data.confirmPassword,
})

/**
 * Traditional email/password login.
 */
export const loginUser = (payload) => apiClient.post('/api/users/login/', payload)

export const mapLoginFormToPayload = (data) => ({
  email: data.email,
  password: data.password,
})

/**
 * Vérifie le code de validation envoyé à l'utilisateur.
 * Expects: { email, code }
 */
export const verifyUserCode = (payload) => apiClient.post('/api/users/verify-code/', payload)

/**
 * Déconnecte l'utilisateur en invalidant le refresh token côté backend.
 * Expects: { refresh }
 */
export const logoutUser = (payload) => apiClient.post('/api/users/logout/', payload)

/**
 * Authentification Google One Tap
 * Expects: { access_token } - L'id_token JWT de Google
 */
export const googleLogin = (payload) => apiClient.post('/api/users/auth/google/', payload) 