<template>
  <div class="password-strength">
    <div
      v-for="rule in rules"
      :key="rule.key"
      class="strength-box"
      :class="{ passed: rule.passed }"
    >
      <span class="icon">
        <svg v-if="rule.passed" width="16" height="16" fill="none" viewBox="0 0 16 16"><path d="M4 8.5l3 3 5-5" stroke="#10b981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        <svg v-else width="16" height="16" fill="none" viewBox="0 0 16 16"><circle cx="8" cy="8" r="7" stroke="#d1d5db" stroke-width="2"/></svg>
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

<style scoped lang="scss">
.password-strength {
  display: flex;
  gap: 12px;
  margin-top: 6px;
  flex-wrap: wrap;
}
.strength-box {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #f3f4f6;
  border-radius: 6px;
  padding: 4px 10px 4px 6px;
  font-size: 13px;
  color: #6b7280;
  transition: background 0.2s, color 0.2s;
  border: 1.5px solid #e5e7eb;
  min-width: 90px;
  font-weight: 500;
}
.strength-box .icon {
  display: flex;
  align-items: center;
}
.strength-box.passed {
  background: #e6f9f1;
  color: #10b981;
  border-color: #10b981;
}
.strength-box.passed .icon svg {
  stroke: #10b981;
}
</style> 