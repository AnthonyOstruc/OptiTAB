<template>
  <svg
    ref="svgRef"
    class="annotation-layer"
    :class="{ 'annotation-layer--draw': editable && activeTool !== 'select' }"
    :style="{ pointerEvents: editable ? 'all' : 'none' }"
    :viewBox="`0 0 ${svgW} ${svgH}`"
    xmlns="http://www.w3.org/2000/svg"
    @mousedown.prevent="onSvgDown"
    @mousemove="onSvgMove"
    @mouseup="onSvgUp"
    @mouseleave="onSvgLeave"
  >
    <defs>
      <marker
        v-for="col in markerColors"
        :key="`m${cid(col)}`"
        :id="`ann-a-${cid(col)}`"
        markerWidth="8"
        markerHeight="6"
        refX="7"
        refY="3"
        orient="auto"
        markerUnits="strokeWidth"
      >
        <polygon points="0 0, 8 3, 0 6" :fill="col" />
      </marker>
    </defs>

    <!-- Existing shapes -->
    <g
      v-for="s in annotations"
      :key="s.id"
      :style="{
        cursor: editable && activeTool === 'select' ? 'move' : 'default',
        pointerEvents: editable ? 'all' : 'none',
        filter: editable && selectedId === s.id ? 'drop-shadow(0 0 5px rgba(255,255,255,0.95))' : 'none',
      }"
      @mousedown.stop="onShapeDown($event, s)"
    >
      <ellipse
        v-if="s.type === 'circle'"
        :cx="toX(s.x)"
        :cy="toY(s.y)"
        :rx="radiusPx(s.width)"
        :ry="radiusPx(s.width)"
        :fill="s.filled ? s.color : 'none'"
        :stroke="s.color"
        :stroke-width="s.strokeWidth"
      />
      <rect
        v-else-if="s.type === 'rect'"
        :x="toX(Math.min(s.x, s.x + s.width))"
        :y="toY(Math.min(s.y, s.y + s.height))"
        :width="Math.abs(wPx(s.width))"
        :height="Math.abs(hPx(s.height))"
        :fill="s.filled ? s.color : 'none'"
        :stroke="s.color"
        :stroke-width="s.strokeWidth"
      />
      <line
        v-else-if="s.type === 'arrow'"
        :x1="toX(s.x)"
        :y1="toY(s.y)"
        :x2="toX(s.x2)"
        :y2="toY(s.y2)"
        :stroke="s.color"
        :stroke-width="s.strokeWidth"
        :marker-end="`url(#ann-a-${cid(s.color)})`"
        stroke-linecap="round"
      />
    </g>

    <!-- Preview while drawing -->
    <g v-if="preview" pointer-events="none" opacity="0.72">
      <ellipse
        v-if="preview.type === 'circle'"
        :cx="toX(preview.x)"
        :cy="toY(preview.y)"
        :rx="radiusPx(preview.width)"
        :ry="radiusPx(preview.width)"
        fill="none"
        :stroke="preview.color"
        :stroke-width="preview.strokeWidth"
        stroke-dasharray="6 3"
      />
      <rect
        v-if="preview.type === 'rect'"
        :x="toX(Math.min(preview.x, preview.x + preview.width))"
        :y="toY(Math.min(preview.y, preview.y + preview.height))"
        :width="Math.abs(wPx(preview.width))"
        :height="Math.abs(hPx(preview.height))"
        fill="none"
        :stroke="preview.color"
        :stroke-width="preview.strokeWidth"
        stroke-dasharray="6 3"
      />
      <line
        v-if="preview.type === 'arrow'"
        :x1="toX(preview.x)"
        :y1="toY(preview.y)"
        :x2="toX(preview.x2)"
        :y2="toY(preview.y2)"
        :stroke="preview.color"
        :stroke-width="preview.strokeWidth"
        :marker-end="`url(#ann-a-${cid(preview.color)})`"
        stroke-linecap="round"
        stroke-dasharray="6 3"
      />
    </g>
  </svg>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'

const BASE_COLORS = ['#e74c3c', '#2980b9', '#f39c12', '#27ae60', '#8e44ad']

const props = defineProps({
  annotations: { type: Array, default: () => [] },
  editable: { type: Boolean, default: false },
  activeTool: { type: String, default: 'select' },
  activeColor: { type: String, default: '#e74c3c' },
  strokeWidth: { type: Number, default: 3 },
  selectedId: { type: String, default: null },
})

const emit = defineEmits(['add', 'update', 'update:selectedId'])

const svgRef = ref(null)
const svgW = ref(300)
const svgH = ref(300)
const preview = ref(null)

let dragOrigin = null
let moveOrigin = null
let ro = null

onMounted(() => {
  updateSize()
  ro = new ResizeObserver(updateSize)
  if (svgRef.value) ro.observe(svgRef.value)
})
onUnmounted(() => ro?.disconnect())

function updateSize() {
  const el = svgRef.value
  if (!el) return
  svgW.value = el.clientWidth || 300
  svgH.value = el.clientHeight || 300
}

function toX(pct) { return (pct / 100) * svgW.value }
function toY(pct) { return (pct / 100) * svgH.value }
function wPx(pct) { return (pct / 100) * svgW.value }
function hPx(pct) { return (pct / 100) * svgH.value }
function radiusPx(pct) { return Math.abs((pct / 100) * svgW.value) }

function svgPt(event) {
  const el = svgRef.value
  if (!el) return { x: 50, y: 50 }
  const r = el.getBoundingClientRect()
  return {
    x: Math.max(0, Math.min(100, ((event.clientX - r.left) / r.width) * 100)),
    y: Math.max(0, Math.min(100, ((event.clientY - r.top) / r.height) * 100)),
  }
}

function cid(color) { return (color || '').replace(/[^a-z0-9]/gi, '') }

function uid() { return Math.random().toString(36).slice(2) + Date.now().toString(36) }

const markerColors = computed(() => {
  const cols = new Set(BASE_COLORS)
  for (const s of props.annotations) if (s.type === 'arrow') cols.add(s.color)
  if (preview.value?.type === 'arrow') cols.add(preview.value.color)
  return [...cols]
})

function buildShape(start, end) {
  const t = props.activeTool
  const color = props.activeColor
  const sw = props.strokeWidth
  if (t === 'circle') {
    const dxPx = ((end.x - start.x) / 100) * svgW.value
    const dyPx = ((end.y - start.y) / 100) * svgH.value
    const rPctW = (Math.hypot(dxPx, dyPx) / svgW.value) * 100
    return { type: 'circle', x: start.x, y: start.y, width: rPctW, color, strokeWidth: sw, filled: false }
  }
  if (t === 'rect') {
    return { type: 'rect', x: start.x, y: start.y, width: end.x - start.x, height: end.y - start.y, color, strokeWidth: sw, filled: false }
  }
  if (t === 'arrow') {
    return { type: 'arrow', x: start.x, y: start.y, x2: end.x, y2: end.y, color, strokeWidth: sw }
  }
  return null
}

function isSignificant(shape) {
  if (!shape) return false
  const MIN = 4
  if (shape.type === 'circle') return radiusPx(shape.width) > MIN
  if (shape.type === 'rect') {
    return Math.abs(wPx(shape.width)) > MIN && Math.abs(hPx(shape.height)) > MIN
  }
  if (shape.type === 'arrow') {
    const dx = ((shape.x2 - shape.x) / 100) * svgW.value
    const dy = ((shape.y2 - shape.y) / 100) * svgH.value
    return Math.hypot(dx, dy) > MIN
  }
  return false
}

function onSvgDown(e) {
  if (!props.editable) return
  if (props.activeTool === 'select') {
    emit('update:selectedId', null)
    return
  }
  dragOrigin = svgPt(e)
}

function onShapeDown(e, shape) {
  if (!props.editable) return
  emit('update:selectedId', shape.id)
  if (props.activeTool !== 'select') return
  dragOrigin = svgPt(e)
  moveOrigin = {
    id: shape.id,
    x: shape.x,
    y: shape.y,
    ...(shape.type === 'arrow' ? { x2: shape.x2, y2: shape.y2 } : {}),
  }
}

function onSvgMove(e) {
  if (!props.editable) return
  const pt = svgPt(e)

  if (dragOrigin && props.activeTool !== 'select') {
    preview.value = buildShape(dragOrigin, pt)
    return
  }

  if (dragOrigin && moveOrigin) {
    const dx = pt.x - dragOrigin.x
    const dy = pt.y - dragOrigin.y
    const shape = props.annotations.find((s) => s.id === moveOrigin.id)
    if (!shape) return
    const moved = { ...shape, x: moveOrigin.x + dx, y: moveOrigin.y + dy }
    if (shape.type === 'arrow') {
      moved.x2 = moveOrigin.x2 + dx
      moved.y2 = moveOrigin.y2 + dy
    }
    emit('update', moved)
  }
}

function onSvgUp(e) {
  if (!props.editable) return
  const pt = svgPt(e)

  if (dragOrigin && props.activeTool !== 'select') {
    const shape = buildShape(dragOrigin, pt)
    if (isSignificant(shape)) {
      const final = { ...shape, id: uid() }
      emit('add', final)
      emit('update:selectedId', final.id)
    }
  }

  dragOrigin = null
  moveOrigin = null
  preview.value = null
}

function onSvgLeave() {
  if (!props.editable) return
  preview.value = null
  dragOrigin = null
  moveOrigin = null
}
</script>

<style scoped>
.annotation-layer {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.annotation-layer--draw {
  cursor: crosshair;
}
</style>
