// Génère les initiales à partir du prénom et du nom (ex: Anthony Tabet => A.T)
export function getInitials(firstName, lastName) {
  const f = firstName ? firstName[0].toUpperCase() : ''
  const l = lastName ? lastName[0].toUpperCase() : ''
  return (f + (l ? '.' + l : '')).trim()
} 