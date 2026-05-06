<template>
  <svg
    ref="svgRef"
    class="annotation-layer"
    :class="{
      'annotation-layer--draw': editable && activeTool !== 'select',
      'annotation-layer--select': editable && activeTool === 'select',
    }"
    :style="{ pointerEvents: editable ? 'all' : 'none' }"
    :viewBox="`0 0 ${svgW} ${svgH}`"
    xmlns="http://www.w3.org/2000/svg"
    @mousedown.prevent="onSvgDown"
    @mousemove="onSvgMove"
    @mouseup="onSvgUp"
    @mouseleave="onSvgLeave"
    @contextmenu.prevent="onSvgContextMenu"
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

    <g
      v-for="s in renderedShapes"
      :key="s.id"
      class="ann-shape"
      :class="{
        'ann-shape--selected': editable && selectedId === s.id,
        'ann-shape--editable': editable && activeTool === 'select',
      }"
      @mousedown.stop="onShapeDown($event, s)"
      @contextmenu.stop.prevent="onShapeContextMenu($event, s)"
    >
      <ellipse
        v-if="s.type === 'circle'"
        :cx="toX(s.x)"
        :cy="toY(s.y)"
        :rx="radiusPx(s.width)"
        :ry="radiusPx(s.width)"
        :fill="s.filled ? s.color : 'transparent'"
        :stroke="s.color"
        :stroke-width="s.strokeWidth"
      />
      <rect
        v-else-if="s.type === 'rect'"
        :x="toX(Math.min(s.x, s.x + s.width))"
        :y="toY(Math.min(s.y, s.y + s.height))"
        :width="Math.abs(wPx(s.width))"
        :height="Math.abs(hPx(s.height))"
        :fill="s.filled ? s.color : 'transparent'"
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

    <!-- Selection bounding box -->
    <g v-if="selectionBox && editable" pointer-events="none">
      <rect
        :x="selectionBox.x"
        :y="selectionBox.y"
        :width="selectionBox.width"
        :height="selectionBox.height"
        fill="none"
        stroke="#1d4ed8"
        :stroke-width="1.4"
        stroke-dasharray="5 3"
      />
    </g>

    <!-- Resize handles -->
    <g v-if="selectionHandles.length && editable">
      <rect
        v-for="h in selectionHandles"
        :key="h.id"
        class="ann-handle"
        :x="h.xPx - HANDLE_HALF"
        :y="h.yPx - HANDLE_HALF"
        :width="HANDLE_SIZE"
        :height="HANDLE_SIZE"
        :rx="h.shape === 'circle' ? HANDLE_HALF : 2"
        :ry="h.shape === 'circle' ? HANDLE_HALF : 2"
        fill="#ffffff"
        stroke="#1d4ed8"
        :stroke-width="1.6"
        :style="{ cursor: h.cursor }"
        @mousedown.stop="onHandleDown($event, h)"
        @contextmenu.stop.prevent
      />
    </g>

    <!-- Drawing preview -->
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

  <Teleport to="body">
    <div
      v-if="contextMenu.open && selectedRendered"
      class="ann-context-menu"
      :style="{ left: `${contextMenu.x}px`, top: `${contextMenu.y}px` }"
      @mousedown.stop
      @click.stop
      @contextmenu.prevent
    >
      <div class="ann-cm-section">
        <span class="ann-cm-label">Couleur</span>
        <div class="ann-cm-colors">
          <button
            v-for="col in BASE_COLORS"
            :key="col"
            class="ann-cm-color"
            :class="{ 'ann-cm-color--active': selectedRendered.color === col }"
            :style="{ background: col }"
            type="button"
            :title="col"
            @click="updateSelectedShape({ color: col })"
          ></button>
        </div>
      </div>

      <div class="ann-cm-section">
        <span class="ann-cm-label">Épaisseur</span>
        <div class="ann-cm-stroke">
          <button
            class="ann-cm-btn"
            type="button"
            aria-label="Diminuer l'épaisseur"
            @click="adjustSelectedStroke(-1)"
          >−</button>
          <span class="ann-cm-stroke-value">{{ selectedRendered.strokeWidth }}px</span>
          <button
            class="ann-cm-btn"
            type="button"
            aria-label="Augmenter l'épaisseur"
            @click="adjustSelectedStroke(1)"
          >+</button>
        </div>
      </div>

      <button
        v-if="selectedRendered.type !== 'arrow'"
        class="ann-cm-toggle"
        :class="{ 'ann-cm-toggle--on': selectedRendered.filled }"
        type="button"
        @click="updateSelectedShape({ filled: !selectedRendered.filled })"
      >
        {{ selectedRendered.filled ? 'Contour seul' : 'Remplir' }}
      </button>

      <button class="ann-cm-delete" type="button" @click="deleteSelected">
        Supprimer
      </button>
    </div>
  </Teleport>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'

const BASE_COLORS = ['#e74c3c', '#2980b9', '#f39c12', '#27ae60', '#8e44ad']
const HANDLE_SIZE = 12
const HANDLE_HALF = HANDLE_SIZE / 2
const MIN_STROKE = 1
const MAX_STROKE = 20

const props = defineProps({
  annotations: { type: Array, default: () => [] },
  editable: { type: Boolean, default: false },
  activeTool: { type: String, default: 'select' },
  activeColor: { type: String, default: '#e74c3c' },
  strokeWidth: { type: Number, default: 3 },
  selectedId: { type: String, default: null },
})

const emit = defineEmits(['add', 'update', 'delete', 'update:selectedId'])

const svgRef = ref(null)
const svgW = ref(300)
const svgH = ref(300)
const preview = ref(null)
const draftShape = ref(null)
const contextMenu = ref({ open: false, x: 0, y: 0 })

let dragOrigin = null
let moveOrigin = null
let resizeOrigin = null
let ro = null

onMounted(() => {
  updateSize()
  ro = new ResizeObserver(updateSize)
  if (svgRef.value) ro.observe(svgRef.value)
  window.addEventListener('mousedown', handleGlobalDown, true)
  window.addEventListener('keydown', handleGlobalKeydown)
})
onUnmounted(() => {
  ro?.disconnect()
  window.removeEventListener('mousedown', handleGlobalDown, true)
  window.removeEventListener('keydown', handleGlobalKeydown)
})

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
function pxToPctX(px) { return svgW.value ? (px / svgW.value) * 100 : 0 }
function pxToPctY(px) { return svgH.value ? (px / svgH.value) * 100 : 0 }

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

const renderedShapes = computed(() => {
  const list = Array.isArray(props.annotations) ? props.annotations : []
  if (!draftShape.value) return list
  return list.map((s) => (s.id === draftShape.value.id ? draftShape.value : s))
})

const selectedRendered = computed(() => {
  if (!props.selectedId) return null
  if (draftShape.value && draftShape.value.id === props.selectedId) return draftShape.value
  return renderedShapes.value.find((s) => s.id === props.selectedId) || null
})

const markerColors = computed(() => {
  const cols = new Set(BASE_COLORS)
  for (const s of renderedShapes.value) if (s.type === 'arrow') cols.add(s.color)
  if (preview.value?.type === 'arrow') cols.add(preview.value.color)
  return [...cols]
})

const selectionBox = computed(() => {
  const s = selectedRendered.value
  if (!s) return null
  if (s.type === 'circle') {
    const r = radiusPx(s.width)
    const cx = toX(s.x), cy = toY(s.y)
    return { x: cx - r, y: cy - r, width: 2 * r, height: 2 * r }
  }
  if (s.type === 'rect') {
    const x = toX(Math.min(s.x, s.x + s.width))
    const y = toY(Math.min(s.y, s.y + s.height))
    return { x, y, width: Math.abs(wPx(s.width)), height: Math.abs(hPx(s.height)) }
  }
  if (s.type === 'arrow') {
    const x1 = toX(s.x), y1 = toY(s.y), x2 = toX(s.x2), y2 = toY(s.y2)
    return {
      x: Math.min(x1, x2),
      y: Math.min(y1, y2),
      width: Math.abs(x2 - x1),
      height: Math.abs(y2 - y1),
    }
  }
  return null
})

const selectionHandles = computed(() => {
  const s = selectedRendered.value
  if (!s) return []
  if (s.type === 'circle') {
    const r = radiusPx(s.width)
    const cx = toX(s.x), cy = toY(s.y)
    return [
      { id: 'circle-e', xPx: cx + r, yPx: cy, cursor: 'ew-resize', shape: 'circle' },
      { id: 'circle-w', xPx: cx - r, yPx: cy, cursor: 'ew-resize', shape: 'circle' },
      { id: 'circle-n', xPx: cx, yPx: cy - r, cursor: 'ns-resize', shape: 'circle' },
      { id: 'circle-s', xPx: cx, yPx: cy + r, cursor: 'ns-resize', shape: 'circle' },
    ]
  }
  if (s.type === 'rect') {
    const minX = Math.min(s.x, s.x + s.width)
    const maxX = Math.max(s.x, s.x + s.width)
    const minY = Math.min(s.y, s.y + s.height)
    const maxY = Math.max(s.y, s.y + s.height)
    const xL = toX(minX), xR = toX(maxX), yT = toY(minY), yB = toY(maxY)
    return [
      { id: 'nw', xPx: xL, yPx: yT, cursor: 'nwse-resize', shape: 'square' },
      { id: 'ne', xPx: xR, yPx: yT, cursor: 'nesw-resize', shape: 'square' },
      { id: 'se', xPx: xR, yPx: yB, cursor: 'nwse-resize', shape: 'square' },
      { id: 'sw', xPx: xL, yPx: yB, cursor: 'nesw-resize', shape: 'square' },
    ]
  }
  if (s.type === 'arrow') {
    return [
      { id: 'arrow-start', xPx: toX(s.x), yPx: toY(s.y), cursor: 'move', shape: 'circle' },
      { id: 'arrow-end', xPx: toX(s.x2), yPx: toY(s.y2), cursor: 'move', shape: 'circle' },
    ]
  }
  return []
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

function clampPct(value) {
  return Math.max(0, Math.min(100, value))
}

function onSvgDown(e) {
  closeContextMenu()
  if (!props.editable) return
  if (props.activeTool === 'select') {
    emit('update:selectedId', null)
    return
  }
  dragOrigin = svgPt(e)
}

function onShapeDown(e, shape) {
  closeContextMenu()
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

function onHandleDown(e, handle) {
  closeContextMenu()
  if (!props.editable) return
  const shape = selectedRendered.value
  if (!shape) return
  resizeOrigin = {
    handle: handle.id,
    shape: { ...shape },
  }
}

function applyResize(pt) {
  const ro = resizeOrigin
  if (!ro) return
  const initial = ro.shape
  const updated = { ...initial }

  if (initial.type === 'circle') {
    const dxPx = ((pt.x - initial.x) / 100) * svgW.value
    const dyPx = ((pt.y - initial.y) / 100) * svgH.value
    const rPx = Math.hypot(dxPx, dyPx)
    updated.width = (rPx / svgW.value) * 100
  } else if (initial.type === 'rect') {
    const minX = Math.min(initial.x, initial.x + initial.width)
    const maxX = Math.max(initial.x, initial.x + initial.width)
    const minY = Math.min(initial.y, initial.y + initial.height)
    const maxY = Math.max(initial.y, initial.y + initial.height)
    const cx = clampPct(pt.x)
    const cy = clampPct(pt.y)
    let nx = initial.x, ny = initial.y, nw = initial.width, nh = initial.height
    if (ro.handle === 'nw') {
      nx = cx; ny = cy; nw = maxX - cx; nh = maxY - cy
    } else if (ro.handle === 'ne') {
      nx = minX; ny = cy; nw = cx - minX; nh = maxY - cy
    } else if (ro.handle === 'se') {
      nx = minX; ny = minY; nw = cx - minX; nh = cy - minY
    } else if (ro.handle === 'sw') {
      nx = cx; ny = minY; nw = maxX - cx; nh = cy - minY
    }
    updated.x = nx
    updated.y = ny
    updated.width = nw
    updated.height = nh
  } else if (initial.type === 'arrow') {
    if (ro.handle === 'arrow-start') {
      updated.x = clampPct(pt.x)
      updated.y = clampPct(pt.y)
    } else if (ro.handle === 'arrow-end') {
      updated.x2 = clampPct(pt.x)
      updated.y2 = clampPct(pt.y)
    }
  }

  draftShape.value = updated
}

function onSvgMove(e) {
  if (!props.editable) return
  const pt = svgPt(e)

  if (resizeOrigin) {
    applyResize(pt)
    return
  }

  if (dragOrigin && !moveOrigin && props.activeTool !== 'select') {
    preview.value = buildShape(dragOrigin, pt)
    return
  }

  if (dragOrigin && moveOrigin) {
    const dx = pt.x - dragOrigin.x
    const dy = pt.y - dragOrigin.y
    const shape = props.annotations.find((s) => s.id === moveOrigin.id)
    if (!shape) return
    const moved = { ...shape, x: clampPct(moveOrigin.x + dx), y: clampPct(moveOrigin.y + dy) }
    if (shape.type === 'arrow') {
      moved.x2 = clampPct(moveOrigin.x2 + dx)
      moved.y2 = clampPct(moveOrigin.y2 + dy)
    }
    draftShape.value = moved
  }
}

function onSvgUp(e) {
  if (!props.editable) return
  const pt = svgPt(e)

  if (dragOrigin && !moveOrigin && !resizeOrigin && props.activeTool !== 'select') {
    const shape = buildShape(dragOrigin, pt)
    if (isSignificant(shape)) {
      const final = { ...shape, id: uid() }
      emit('add', final)
      emit('update:selectedId', final.id)
    }
  }

  if (draftShape.value) {
    emit('update', { ...draftShape.value })
  }

  dragOrigin = null
  moveOrigin = null
  resizeOrigin = null
  preview.value = null
  draftShape.value = null
}

function onSvgLeave() {
  if (!props.editable) return
  if (draftShape.value) {
    emit('update', { ...draftShape.value })
  }
  preview.value = null
  dragOrigin = null
  moveOrigin = null
  resizeOrigin = null
  draftShape.value = null
}

function onSvgContextMenu(e) {
  closeContextMenu()
  if (!props.editable) return
  emit('update:selectedId', null)
}

function onShapeContextMenu(e, shape) {
  if (!props.editable) return
  emit('update:selectedId', shape.id)
  contextMenu.value = { open: true, x: e.clientX, y: e.clientY }
}

function closeContextMenu() {
  if (contextMenu.value.open) {
    contextMenu.value = { open: false, x: 0, y: 0 }
  }
}

function updateSelectedShape(patch) {
  const shape = selectedRendered.value
  if (!shape) return
  emit('update', { ...shape, ...patch })
}

function adjustSelectedStroke(delta) {
  const shape = selectedRendered.value
  if (!shape) return
  const next = Math.min(MAX_STROKE, Math.max(MIN_STROKE, (shape.strokeWidth || 1) + delta))
  if (next === shape.strokeWidth) return
  emit('update', { ...shape, strokeWidth: next })
}

function deleteSelected() {
  if (!props.selectedId) return
  emit('delete', props.selectedId)
  closeContextMenu()
}

function handleGlobalDown(event) {
  if (!contextMenu.value.open) return
  const target = event.target
  if (target && target.closest && target.closest('.ann-context-menu')) return
  closeContextMenu()
}

function handleGlobalKeydown(event) {
  if (event.key === 'Escape' && contextMenu.value.open) {
    closeContextMenu()
  }
}
</script>

<style scoped>
.annotation-layer {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 2;
}

.annotation-layer--draw {
  cursor: crosshair;
}

.annotation-layer--select {
  cursor: default;
}

.ann-shape {
  transition: filter 0.12s ease;
}

.ann-shape--editable {
  cursor: move;
}

.ann-shape--editable:hover {
  filter: brightness(1.06) drop-shadow(0 0 3px rgba(29, 78, 216, 0.45));
}

.ann-shape--selected {
  filter: drop-shadow(0 0 4px rgba(29, 78, 216, 0.65));
}

.ann-handle {
  pointer-events: all;
  filter: drop-shadow(0 1px 2px rgba(15, 23, 42, 0.4));
}

.ann-handle:hover {
  fill: #dbeafe;
}
</style>

<style>
.ann-context-menu {
  position: fixed;
  z-index: 27500;
  min-width: 200px;
  background: #ffffff;
  border: 1px solid #bfdbfe;
  border-radius: 12px;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.32);
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-family: inherit;
}

.ann-cm-section {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.ann-cm-label {
  color: #1e3a8a;
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.ann-cm-colors {
  display: flex;
  align-items: center;
  gap: 6px;
}

.ann-cm-color {
  width: 22px;
  height: 22px;
  border: 2px solid transparent;
  border-radius: 50%;
  cursor: pointer;
  flex-shrink: 0;
  transition: transform 0.12s, border-color 0.12s;
}

.ann-cm-color:hover {
  transform: scale(1.16);
}

.ann-cm-color--active {
  border-color: #ffffff;
  box-shadow: 0 0 0 2px #1d4ed8;
}

.ann-cm-stroke {
  display: flex;
  align-items: center;
  gap: 6px;
}

.ann-cm-btn {
  border: 0;
  border-radius: 6px;
  background: #eff6ff;
  color: #1e40af;
  font-size: 13px;
  font-weight: 800;
  line-height: 1;
  padding: 6px 9px;
  cursor: pointer;
  min-width: 28px;
}

.ann-cm-btn:hover {
  background: #dbeafe;
}

.ann-cm-stroke-value {
  min-width: 38px;
  text-align: center;
  color: #1e3a8a;
  font-size: 12px;
  font-weight: 800;
}

.ann-cm-toggle {
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  background: #f8fbff;
  color: #1e3a8a;
  font-size: 12px;
  font-weight: 800;
  padding: 7px 10px;
  cursor: pointer;
}

.ann-cm-toggle:hover {
  background: #eff6ff;
}

.ann-cm-toggle--on {
  background: #1d4ed8;
  color: #ffffff;
  border-color: #1d4ed8;
}

.ann-cm-toggle--on:hover {
  background: #1e40af;
}

.ann-cm-delete {
  border: 0;
  border-radius: 8px;
  background: #fee2e2;
  color: #991b1b;
  font-size: 12px;
  font-weight: 800;
  padding: 8px 10px;
  cursor: pointer;
}

.ann-cm-delete:hover {
  background: #fecaca;
}
</style>
