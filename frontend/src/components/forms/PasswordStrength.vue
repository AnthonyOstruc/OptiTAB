<template>
  <div class="password-strength">
    <div
      v-for="rule in rules"
      :key="rule.key"
      class="strength-box"
      :class="{ passed: rule.passed }"
    >
      <span class="icon">
        <svg v-if="rule.passed" width="16" height="16" fill="none" viewBox="0 0 16 16"><path d="M4 8.5l3 3 5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        <svg v-else width="16" height="16" fill="none" viewBox="0 0 16 16"><circle cx="8" cy="8" r="7" stroke="currentColor" stroke-width="2"/></svg>
      </span>
      <span class="label">{{ rule.label }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PasswordStrength',
  props: {
    password: {
      type: String,
      required: true
    }
  },
  computed: {
    rules() {
      const pwd = this.password || ''
      return [
        {
          key: 'length',
          label: '8+ caractères',
          passed: pwd.length >= 8
        },
        {
          key: 'uppercase',
          label: 'Majuscule',
          passed: /[A-Z]/.test(pwd)
        },
        {
          key: 'lowercase',
          label: 'Minuscule',
          passed: /[a-z]/.test(pwd)
        },
        {
          key: 'digit',
          label: 'Chiffre',
          passed: /\d/.test(pwd)
        },
        {
          key: 'special',
          label: 'Caractère spécial',
          passed: /[^A-Za-z0-9]/.test(pwd)
        }
      ]
    }
  }
}
</script>

<style scoped>
/* Critères du mot de passe : pastilles discrètes, vertes une fois remplies. */
.password-strength {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 2px;
}
.strength-box {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 4px 10px 4px 7px;
  border-radius: 999px;
  background: var(--om-bg-soft, #f6f8fc);
  color: var(--om-muted, #5d667d);
  font-family: var(--om-font, 'Montserrat', sans-serif);
  font-size: 12.5px;
  font-weight: 600;
  transition: background 0.2s, color 0.2s;
}
.strength-box .icon {
  display: flex;
  align-items: center;
  color: var(--om-line-strong, #cfd6e4);
}
.strength-box.passed {
  background: var(--om-green-50, #ecf7ec);
  color: var(--om-green-700, #2f7a3a);
}
.strength-box.passed .icon {
  color: var(--om-green-700, #2f7a3a);
}
.strength-box .icon svg {
  width: 14px;
  height: 14px;
}
</style>
