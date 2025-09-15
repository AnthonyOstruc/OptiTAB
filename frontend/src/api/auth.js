import apiClient from './client'

/**
 * Register a new user
 */
export const registerUser = (payload) =>
  apiClient.post('/api/users/register/', payload, { timeout: 20000 })

export const mapRegisterFormToPayload = (data) => ({
  first_name: data.firstName?.trim(),
  last_name: data.lastName?.trim(),
  email: data.email?.trim().toLowerCase(),
  password: data.password,
  password_confirmation: data.confirmPassword,
})

/**
 * Email/password login
 */
export const loginUser = (payload) =>
  apiClient.post('/api/users/login/', {
    email: (payload?.email || '').trim().toLowerCase(),
    password: payload?.password,
  }, { timeout: 20000 })

export const mapLoginFormToPayload = (data) => ({
  email: data.email?.trim().toLowerCase(),
  password: data.password,
})

/**
 * Verify validation code
 */
export const verifyUserCode = (payload) =>
  apiClient.post('/api/users/verify-code/', payload, { timeout: 15000 })

/**
 * Logout (blacklist refresh token)
 */
export const logoutUser = (payload) =>
  apiClient.post('/api/users/logout/', payload, { timeout: 10000 })

/**
 * Google OAuth login (One Tap)
 */
export const googleLogin = (payload) =>
  apiClient.post('/api/users/auth/google/', payload, { timeout: 20000 })


/**
 * Request password reset link
 */
export const requestPasswordReset = (payload) => {
  const email = (payload?.email || '').trim().toLowerCase()
  return apiClient.post('/api/users/password/reset/', { email }, { timeout: 15000 })
}

/**
 * Confirm password reset (set new password using token)
 * django_rest_passwordreset expects: token, password
 */
export const confirmPasswordReset = ({ token, password }) => {
  return apiClient.post('/api/users/password/reset/confirm/', { token, password }, { timeout: 15000 })
}


