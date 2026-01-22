<template>
  <div class="calculator">
    <div class="calc-tabs">
      <button :class="['calc-tab', { active: mode === 'basic' }]" @click="mode = 'basic'">
        Algèbre
      </button>
      <button :class="['calc-tab', { active: mode === 'trig' }]" @click="mode = 'trig'">
        Trigonométrie
      </button>
    </div>

    <div class="calc-body">
      <!-- Mode Algèbre -->
      <template v-if="mode === 'basic'">
        <div class="calc-row">
          <button class="calc-btn fn" @click="insert('\\frac{}{}')">
            <svg viewBox="0 0 24 24"><rect x="7" y="2" width="10" height="7" rx="1.5"/><line x1="4" y1="12" x2="20" y2="12" stroke-width="2"/><rect x="7" y="15" width="10" height="7" rx="1.5"/></svg>
          </button>
          <button class="calc-btn fn" @click="insert('^{}')">
            <svg viewBox="0 0 24 24"><rect x="2" y="9" width="12" height="12" rx="1.5"/><rect x="15" y="2" width="7" height="7" rx="1.5"/></svg>
          </button>
          <button class="calc-btn fn" @click="insert('\\sqrt{}')">
            <svg viewBox="0 0 24 24"><path d="M1 14 L5 20 L9 4 L23 4"/><rect x="13" y="8" width="8" height="8" rx="1.5"/></svg>
          </button>
          <button class="calc-btn fn" @click="insert('\\sqrt[{}]{}')">
            <svg viewBox="0 0 24 24"><rect x="2.1" y="3.2" width="5.0" height="5.0" rx="1.0"/><path d="M5.6 12.4 L7.8 18.4 L10.0 6.4 L21.2 6.4"/><rect x="13.6" y="10.0" width="7.2" height="7.2" rx="1.0"/></svg>
          </button>
          <button class="calc-btn fn" @click="insert('\\log_{}')">log</button>
        </div>

        <div class="calc-row">
          <button class="calc-btn fn" @click="insert('|{}|')">|□|</button>
          <button class="calc-btn fn" @click="insert('\\lfloor{}\\rfloor')">⌊□⌋</button>
          <button class="calc-btn fn" @click="insert('\\lceil{}\\rceil')">⌈□⌉</button>
          <button class="calc-btn fn" @click="insert('{}!')">□!</button>
          <button class="calc-btn fn" @click="insert('\\ln')">ln</button>
        </div>

        <div class="calc-row">
          <button class="calc-btn" @click="insert('(')">(</button>
          <button class="calc-btn" @click="insert(')')">)</button>
          <button class="calc-btn" @click="insert('\\pi')">π</button>
          <button class="calc-btn" @click="insert('e')">e</button>
          <button class="calc-btn" @click="insert('x')">x</button>
        </div>

        <div class="calc-row">
          <button class="calc-btn digit" @click="insert('7')">7</button>
          <button class="calc-btn digit" @click="insert('8')">8</button>
          <button class="calc-btn digit" @click="insert('9')">9</button>
          <button class="calc-btn delete" @click="emit('backspace')">⌫</button>
          <button class="calc-btn clear" @click="insert({ type: 'clear' })">AC</button>
        </div>

        <div class="calc-row">
          <button class="calc-btn digit" @click="insert('4')">4</button>
          <button class="calc-btn digit" @click="insert('5')">5</button>
          <button class="calc-btn digit" @click="insert('6')">6</button>
          <button class="calc-btn operator" @click="insert('\\div')">÷</button>
          <button class="calc-btn operator" @click="insert('\\times')">×</button>
        </div>

        <div class="calc-row">
          <button class="calc-btn digit" @click="insert('1')">1</button>
          <button class="calc-btn digit" @click="insert('2')">2</button>
          <button class="calc-btn digit" @click="insert('3')">3</button>
          <button class="calc-btn operator" @click="insert('-')">−</button>
          <button class="calc-btn operator" @click="insert('+')">+</button>
        </div>

        <div class="calc-row">
          <button class="calc-btn digit" @click="insert('0')">0</button>
          <button class="calc-btn" @click="insert('.')">.</button>
          <button class="calc-btn" @click="insert('=')">=</button>
          <button class="calc-btn arrow" @click="emit('moveLeft')">←</button>
          <button class="calc-btn arrow" @click="emit('moveRight')">→</button>
        </div>

        <div class="calc-row last-row">
          <button class="calc-btn" @click="insert('\\le')">≤</button>
          <button class="calc-btn" @click="insert('\\ge')">≥</button>
          <button class="calc-btn" @click="insert('\\infty')">∞</button>
          <button class="calc-btn execute" @click="emit('calculate')">▶</button>
        </div>
      </template>

      <!-- Mode Trigonométrie -->
      <template v-else>
        <div class="calc-row">
          <button class="calc-btn fn" @click="insert('\\sin')">sin</button>
          <button class="calc-btn fn" @click="insert('\\cos')">cos</button>
          <button class="calc-btn fn" @click="insert('\\tan')">tan</button>
          <button class="calc-btn fn" @click="insert('\\cot')">cot</button>
          <button class="calc-btn fn" @click="insert('°')">°</button>
        </div>

        <div class="calc-row">
          <button class="calc-btn fn" @click="insert('\\arcsin')">sin⁻¹</button>
          <button class="calc-btn fn" @click="insert('\\arccos')">cos⁻¹</button>
          <button class="calc-btn fn" @click="insert('\\arctan')">tan⁻¹</button>
          <button class="calc-btn fn" @click="insert('\\text{arccot}')">cot⁻¹</button>
          <button class="calc-btn" @click="insert('x')">x</button>
        </div>

        <div class="calc-row">
          <button class="calc-btn" @click="insert('\\pi')">π</button>
          <button class="calc-btn" @click="insert('\\frac{\\pi}{2}')">π/2</button>
          <button class="calc-btn" @click="insert('\\frac{\\pi}{3}')">π/3</button>
          <button class="calc-btn" @click="insert('\\frac{\\pi}{4}')">π/4</button>
          <button class="calc-btn" @click="insert('\\frac{\\pi}{6}')">π/6</button>
        </div>

        <div class="calc-row">
          <button class="calc-btn" @click="insert('2\\pi')">2π</button>
          <button class="calc-btn" @click="insert('\\theta')">θ</button>
          <button class="calc-btn" @click="insert('\\alpha')">α</button>
          <button class="calc-btn" @click="insert('\\beta')">β</button>
          <button class="calc-btn" @click="insert('\\gamma')">γ</button>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['insert', 'backspace', 'submit', 'calculate', 'moveLeft', 'moveRight'])
const mode = ref('basic')

const insert = (val) => emit('insert', val)
</script>

<style scoped>
.calculator {
  width: 100%;
  max-width: 420px;
  margin: 12px auto;
  background: #1c1c1e;
  border-radius: 16px;
  padding: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.calc-tabs {
  display: flex;
  gap: 5px;
  margin-bottom: 10px;
}

.calc-tab {
  flex: 1;
  padding: 8px;
  border: none;
  border-radius: 8px;
  background: #2c2c2e;
  color: #8e8e93;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.calc-tab:hover {
  background: #3a3a3c;
}

.calc-tab.active {
  background: #0a84ff;
  color: #fff;
}

.calc-body {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.calc-row {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 6px;
}

.calc-btn {
  height: 42px;
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 500;
  background: #2c2c2e;
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', system-ui, sans-serif;
}

.calc-btn:hover {
  background: #3a3a3c;
  transform: scale(1.02);
}

.calc-btn:active {
  transform: scale(0.96);
  background: #48484a;
}

/* Chiffres */
.calc-btn.digit {
  background: #505050;
  font-size: 18px;
  font-weight: 500;
}

.calc-btn.digit:hover {
  background: #636366;
}

/* Opérateurs */
.calc-btn.operator {
  background: #ff9f0a;
  color: #000;
  font-size: 20px;
  font-weight: 600;
}

.calc-btn.operator:hover {
  background: #ffb340;
}

/* Fonctions */
.calc-btn.fn {
  background: #3a3a3c;
  font-size: 13px;
}

.calc-btn.fn:hover {
  background: #48484a;
}

.calc-btn.fn svg {
  width: 18px;
  height: 18px;
  stroke: #fff;
  stroke-width: 2;
  fill: none;
}

/* Suppression */
.calc-btn.delete {
  background: #ff9f0a;
  color: #000;
  font-size: 15px;
}

.calc-btn.delete:hover {
  background: #ffb340;
}

/* Clear */
.calc-btn.clear {
  background: #ff453a;
  color: #fff;
  font-size: 12px;
  font-weight: 600;
}

.calc-btn.clear:hover {
  background: #ff6961;
}

/* Navigation */
.calc-btn.arrow {
  background: #636366;
  font-size: 15px;
}

.calc-btn.arrow:hover {
  background: #8e8e93;
}

/* Entrée */
.calc-btn.submit {
  background: #30d158;
  color: #000;
  font-size: 16px;
}

.calc-btn.submit:hover {
  background: #4cd964;
}

/* Exécution */
.calc-btn.execute {
  background: #0a84ff;
  color: #fff;
  font-size: 14px;
}

.calc-btn.execute:hover {
  background: #409cff;
}

/* Dernière ligne avec bouton large */
.calc-row.last-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 2fr;
  gap: 6px;
}

/* Responsive */
@media (max-width: 540px) {
  .calculator {
    margin: 10px;
    padding: 12px;
    border-radius: 16px;
  }

  .calc-tabs {
    gap: 4px;
    margin-bottom: 10px;
  }

  .calc-tab {
    padding: 8px;
    font-size: 12px;
    border-radius: 8px;
  }

  .calc-body {
    gap: 6px;
  }

  .calc-row {
    gap: 6px;
  }

  .calc-btn {
    height: 44px;
    font-size: 15px;
    border-radius: 10px;
  }

  .calc-btn.digit {
    font-size: 18px;
  }

  .calc-btn.operator {
    font-size: 20px;
  }

  .calc-btn.fn {
    font-size: 13px;
  }

  .calc-btn.fn svg {
    width: 18px;
    height: 18px;
  }
}
</style>
