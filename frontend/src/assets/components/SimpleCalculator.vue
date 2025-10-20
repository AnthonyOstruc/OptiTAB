<template>
  <div class="simple-calculator">
    <div v-if="tabsList.length > 1" class="calc-tabs">
      <button
        v-for="tab in tabsList"
        :key="tab"
        :class="['calc-tab', { active: tab === activeTab }]"
        @click="activeTab = tab"
      >
        {{ tab }}
      </button>
    </div>
    <div class="calc-grid">
      <template v-for="(row, rowIdx) in currentLayout" :key="rowIdx">
        <div class="calc-row">
          <template v-for="(btn, colIdx) in row" :key="colIdx">
            <button
              class="calc-btn"
              :class="[btn.class, btn.slot ? 'btn-svg-foreground' : '']"
              @click="onButtonClick(btn)"
            >
              <slot v-if="btn.slot" :name="btn.slot" />
              <template v-else-if="btn.icon">
                <component :is="btn.icon" />
              </template>
              <span v-else>{{ btn.label }}</span>
            </button>
          </template>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  tabs: {
    type: Object,
    required: true
  },
  defaultTab: {
    type: String,
    default: ''
  }
})

const tabsList = computed(() => Object.keys(props.tabs))
const activeTab = ref(props.defaultTab && props.tabs[props.defaultTab] ? props.defaultTab : tabsList.value[0])

// Watch tabs prop and reset activeTab if needed
watch(
  () => props.tabs,
  (newTabs) => {
    const keys = Object.keys(newTabs)
    if (!keys.includes(activeTab.value)) {
      activeTab.value = keys[0]
    }
  },
  { immediate: true, deep: true }
)

const currentLayout = computed(() => props.tabs[activeTab.value] || [])

const emit = defineEmits(['input', 'result'])

function onButtonClick(btn) {
  if (btn.action === 'clear') {
    emit('input', { type: 'clear' })
  } else if (btn.action === 'equals') {
    emit('input', { type: 'equals' })
  } else if (btn.insert !== undefined) {
    emit('input', btn.insert)
  } else if (btn.value !== undefined) {
    emit('input', btn.value)
  }
}
</script>

<style scoped>
.simple-calculator {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.calc-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  justify-content: center;
}
.calc-tab {
  padding: 0.4rem 1.2rem;
  border: none;
  background: #f1f5f9;
  color: #1e293b;
  font-size: 1rem;
  border-radius: 4px 4px 0 0;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.2s, color 0.2s;
}
.calc-tab.active {
  background: #2563eb;
  color: #fff;
}
.calc-grid {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
.calc-row {
  display: flex;
  gap: 0.25rem;
}
.calc-btn {
  flex: 1 1 0;
  flex-basis: 38px;
  max-width: 48px;
  min-width: 32px;
  min-height: 38px;
  padding: 0.28rem;
  font-size: 1rem;
  border: 1.5px solid #b6c2d1;
  border-radius: 6px;
  background: #f8fafc;
  cursor: pointer;
  transition: background 0.18s, box-shadow 0.18s, color 0.18s, border-color 0.18s;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  color: #1e293b;
}
.calc-btn:hover, .calc-btn:focus {
  background: #e0e7ef;
  border-color: #2563eb;
  box-shadow: 0 2px 8px 0 rgba(37,99,235,0.07);
  outline: none;
  color: #193e8e;
}
.calc-btn:active {
  background: #dbeafe;
  color: #2563eb;
  box-shadow: 0 1px 4px 0 rgba(37,99,235,0.12);
  transform: scale(0.97);
}
.btn-svg-foreground {
  overflow: visible;
}
.btn-svg-foreground .svg-dark {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  z-index: 1;
  pointer-events: none;
}
</style> 