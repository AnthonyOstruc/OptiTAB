<template>
  <figure class="dv">
    <div class="dv-laptop">
      <div class="dv-laptop__lid">
        <span class="dv-laptop__cam" aria-hidden="true"></span>
        <div class="dv-laptop__screen">
          <video
            ref="laptopRef"
            class="dv-video"
            muted
            loop
            playsinline
            preload="none"
            disablepictureinpicture
            :poster="DEMOS.ordinateur.poster"
            width="1536"
            height="960"
            aria-hidden="true"
          >
            <source :src="DEMOS.ordinateur.webm" type="video/webm" />
            <source :src="DEMOS.ordinateur.mp4" type="video/mp4" />
          </video>
          <button type="button" class="dv-zoom" :aria-label="`Voir en grand : ${DEMOS.ordinateur.label}`" @click="openZoom('ordinateur')">
            <span class="dv-zoom__pill"><ArrowsPointingOutIcon aria-hidden="true" />Voir en grand</span>
          </button>
        </div>
      </div>
      <div class="dv-laptop__base" aria-hidden="true"><span></span></div>
    </div>

    <div class="dv-phone">
      <div class="dv-phone__screen">
        <div class="dv-phone__status" aria-hidden="true">
          <span class="dv-phone__time">9:41</span>
          <span class="dv-phone__island"></span>
          <span class="dv-phone__icons">
            <svg viewBox="0 0 18 12"><rect x="0" y="8" width="3" height="4" rx="1" /><rect x="5" y="5.5" width="3" height="6.5" rx="1" /><rect x="10" y="3" width="3" height="9" rx="1" /><rect x="15" y="0" width="3" height="12" rx="1" /></svg>
            <svg viewBox="0 0 16 12"><path d="M8 12 5.3 9.2a3.8 3.8 0 0 1 5.4 0Z" /><path d="M2.6 6.5 4.1 8a5.5 5.5 0 0 1 7.8 0l1.5-1.5a7.6 7.6 0 0 0-10.8 0Z" /><path d="M0 3.9 1.5 5.4a9.2 9.2 0 0 1 13 0L16 3.9a11.3 11.3 0 0 0-16 0Z" /></svg>
            <svg viewBox="0 0 27 12"><rect x="0.5" y="0.5" width="22" height="11" rx="3.2" fill="none" stroke="currentColor" opacity=".4" /><rect x="2" y="2" width="19" height="8" rx="2" /><rect x="24" y="4" width="2" height="4" rx="1" opacity=".45" /></svg>
          </span>
        </div>
        <div class="dv-phone__view">
          <video
            ref="phoneRef"
            class="dv-video"
            muted
            loop
            playsinline
            preload="none"
            disablepictureinpicture
            :poster="DEMOS.telephone.poster"
            width="780"
            height="1688"
            aria-hidden="true"
          >
            <source :src="DEMOS.telephone.webm" type="video/webm" />
            <source :src="DEMOS.telephone.mp4" type="video/mp4" />
          </video>
          <button type="button" class="dv-zoom" :aria-label="`Voir en grand : ${DEMOS.telephone.label}`" @click="openZoom('telephone')">
            <span class="dv-zoom__pill"><ArrowsPointingOutIcon aria-hidden="true" />Voir en grand</span>
          </button>
        </div>
      </div>
    </div>
  </figure>

  <Teleport to="body">
    <Transition name="dv-lb">
      <div
        v-if="zoom"
        class="dv-lb"
        role="dialog"
        aria-modal="true"
        :aria-label="DEMOS[zoom].label"
        @click.self="closeZoom"
      >
        <button ref="closeRef" type="button" class="dv-lb__close" aria-label="Fermer la démonstration" @click="closeZoom">
          <XMarkIcon aria-hidden="true" />
        </button>
        <div :class="['dv-lb__frame', `dv-lb__frame--${zoom}`]">
          <video
            class="dv-lb__video"
            :autoplay="!reducedMotion"
            muted
            loop
            playsinline
            controls
            disablepictureinpicture
            :poster="DEMOS[zoom].poster"
          >
            <source :src="DEMOS[zoom].webm" type="video/webm" />
            <source :src="DEMOS[zoom].mp4" type="video/mp4" />
          </video>
        </div>
        <p class="dv-lb__caption">{{ DEMOS[zoom].caption }}</p>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, watch, nextTick, onMounted, onBeforeUnmount } from 'vue'
import { ArrowsPointingOutIcon, XMarkIcon } from '@heroicons/vue/24/outline'

const DEMOS = {
  ordinateur: {
    webm: '/video/optitab-demo-ordinateur.webm',
    mp4: '/video/optitab-demo-ordinateur.mp4',
    poster: '/video/optitab-demo-ordinateur-poster.jpg',
    label: 'démonstration sur ordinateur',
    caption: 'Sur ordinateur · Terminale, chapitre « Calcul intégral »'
  },
  telephone: {
    webm: '/video/optitab-demo-telephone.webm',
    mp4: '/video/optitab-demo-telephone.mp4',
    poster: '/video/optitab-demo-telephone-poster.jpg',
    label: 'démonstration sur téléphone',
    caption: 'Sur téléphone · Terminale, chapitre « Probabilités conditionnelles »'
  }
}

const laptopRef = ref(null)
const phoneRef = ref(null)
const closeRef = ref(null)
const zoom = ref(null)
const reducedMotion = ref(false)
let observer = null
const visible = new Set()

const playVisible = () => {
  ;[laptopRef.value, phoneRef.value].forEach((video) => {
    if (!video) return
    if (!zoom.value && !reducedMotion.value && visible.has(video)) video.play?.().catch(() => {})
    else video.pause?.()
  })
}

const openZoom = (key) => {
  zoom.value = key
}

const closeZoom = () => {
  zoom.value = null
}

const onKeydown = (event) => {
  if (event.key === 'Escape' && zoom.value) closeZoom()
}

// La démo agrandie met en pause les vidéos de la page et bloque le défilement.
watch(zoom, async (value) => {
  document.documentElement.classList.toggle('vt-scroll-lock', Boolean(value))
  playVisible()
  if (value) {
    await nextTick()
    closeRef.value?.focus()
  }
})

// Chaque vidéo ne se charge et ne joue que lorsqu'elle est à l'écran.
// Une vidéo masquée (l'ordinateur sur téléphone) n'est donc jamais téléchargée.
onMounted(() => {
  reducedMotion.value = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false
  window.addEventListener('keydown', onKeydown)
  if (!('IntersectionObserver' in window)) return
  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(({ target, isIntersecting }) => {
        if (isIntersecting) visible.add(target)
        else visible.delete(target)
      })
      playVisible()
    },
    { threshold: 0.2 }
  )
  ;[laptopRef.value, phoneRef.value].forEach((video) => video && observer.observe(video))
})

onBeforeUnmount(() => {
  observer?.disconnect()
  observer = null
  window.removeEventListener('keydown', onKeydown)
  document.documentElement.classList.remove('vt-scroll-lock')
})
</script>

<style scoped>
/* Les marges latérales laissent la place au socle de l'ordinateur,
   plus large que l'écran, pour qu'il ne soit jamais coupé. */
.dv {
  position: relative;
  margin: 0;
  padding: 0 9% 5% 6%;
}

.dv-video {
  display: block;
  width: 100%;
  height: auto;
  background: #fff;
}

/* Zone cliquable posée sur l'écran : ouvre la démo en grand. */
.dv-zoom {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: flex-end;
  justify-content: flex-end;
  padding: 3%;
  border: 0;
  background: transparent;
  cursor: zoom-in;
}

.dv-zoom__pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 12px;
  border-radius: 999px;
  background: rgba(13, 31, 79, 0.86);
  color: #fff;
  font-family: var(--vt-font, 'Montserrat', sans-serif);
  font-size: 13px;
  font-weight: 700;
  line-height: 1;
  white-space: nowrap;
  box-shadow: 0 6px 16px rgba(13, 31, 79, 0.25);
  transition: transform 0.15s ease, background-color 0.15s ease;
}

.dv-zoom__pill svg {
  width: 15px;
  height: 15px;
}

.dv-zoom:hover .dv-zoom__pill,
.dv-zoom:focus-visible .dv-zoom__pill {
  background: #0d1f4f;
  transform: scale(1.05);
}

.dv-zoom:focus-visible {
  outline: 3px solid rgba(95, 172, 96, 0.7);
  outline-offset: -3px;
}

/* ---------- Ordinateur ---------- */

.dv-laptop {
  position: relative;
}

.dv-laptop__lid {
  position: relative;
  padding: 3.1% 2.3% 2.4%;
  border-radius: 14px 14px 4px 4px;
  background: #101318;
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.08),
    0 0 0 1.5px #c7ccd4,
    0 30px 60px -20px rgba(16, 32, 79, 0.35);
}

.dv-laptop__cam {
  position: absolute;
  top: 1.15%;
  left: 50%;
  width: 0.7%;
  aspect-ratio: 1;
  border-radius: 50%;
  background: #2a2f38;
  transform: translateX(-50%);
}

.dv-laptop__screen {
  position: relative;
  overflow: hidden;
  border-radius: 3px;
  background: #fff;
}

.dv-laptop__base {
  position: relative;
  width: 114%;
  height: 0;
  margin-left: -7%;
  padding-bottom: 3.6%;
  border-radius: 2px 2px 18px 18px / 2px 2px 100% 100%;
  background: linear-gradient(180deg, #e9ecf1 0%, #c9ced6 55%, #a9afb9 100%);
  box-shadow: 0 18px 30px -12px rgba(16, 32, 79, 0.35);
}

.dv-laptop__base span {
  position: absolute;
  top: 0;
  left: 50%;
  width: 15%;
  height: 42%;
  border-radius: 0 0 10px 10px;
  background: linear-gradient(180deg, #b7bcc5, #cfd3da);
  transform: translateX(-50%);
}

/* ---------- Téléphone ---------- */

.dv-phone {
  position: absolute;
  right: 0;
  bottom: 0;
  width: 26%;
  padding: 2.6%;
  border-radius: 17% / 7.8%;
  background: #101318;
  box-shadow:
    inset 0 0 0 1.5px #3a3f48,
    0 0 0 1.5px #c7ccd4,
    0 28px 50px -14px rgba(16, 32, 79, 0.45);
  container-type: inline-size;
}

.dv-phone__screen {
  overflow: hidden;
  border-radius: 13% / 6%;
  background: #fff;
}

.dv-phone__view {
  position: relative;
}

/* Sur l'ordinateur, le bouton passe à gauche : à droite, le téléphone le cacherait. */
.dv-laptop .dv-zoom {
  justify-content: flex-start;
}

.dv-phone .dv-zoom {
  padding: 5%;
}

.dv-phone .dv-zoom__pill {
  padding: 6px 10px;
  font-size: 12px;
}

.dv-phone__status {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  aspect-ratio: 390 / 50;
  padding: 0 7%;
  background: #fff;
  color: #111;
}

.dv-phone__time {
  font-family: -apple-system, 'SF Pro Text', 'Segoe UI', system-ui, sans-serif;
  font-size: 4.2cqw;
  font-weight: 600;
  letter-spacing: -0.01em;
}

.dv-phone__island {
  width: 31cqw;
  height: 9cqw;
  border-radius: 999px;
  background: #000;
}

.dv-phone__icons {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 1.4cqw;
}

.dv-phone__icons svg {
  height: 3.1cqw;
  width: auto;
  fill: currentColor;
}

/* Sur téléphone, seule la démo téléphone est affichée (et donc chargée). */
@media (max-width: 640px) {
  .dv {
    padding: 0;
  }

  .dv-laptop {
    display: none;
  }

  .dv-phone {
    position: relative;
    width: min(76%, 300px);
    margin: 0 auto;
    padding: 3.2%;
  }
}

/* ---------- Démo en grand ---------- */

.dv-lb {
  position: fixed;
  inset: 0;
  z-index: 12800;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 14px;
  padding: 56px 24px 24px;
  background: rgba(8, 14, 32, 0.9);
}

.dv-lb__close {
  position: absolute;
  top: calc(12px + env(safe-area-inset-top, 0px));
  right: 12px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 46px;
  height: 46px;
  border: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
  cursor: pointer;
}

.dv-lb__close:hover,
.dv-lb__close:focus-visible {
  background: rgba(255, 255, 255, 0.22);
  outline: none;
}

.dv-lb__close svg {
  width: 26px;
  height: 26px;
}

.dv-lb__frame {
  overflow: hidden;
  background: #fff;
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.45);
}

.dv-lb__frame--ordinateur {
  width: min(1280px, 100%, calc((100vh - 140px) * 1.6));
  border-radius: 12px;
}

.dv-lb__frame--telephone {
  width: min(420px, 100%, calc((100vh - 140px) * 0.462));
  border-radius: 28px;
}

.dv-lb__video {
  display: block;
  width: 100%;
  height: auto;
}

.dv-lb__caption {
  max-width: 720px;
  margin: 0;
  text-align: center;
  font-family: var(--vt-font, 'Montserrat', sans-serif);
  font-size: 14px;
  font-weight: 500;
  line-height: 1.5;
  color: rgba(255, 255, 255, 0.78);
}

.dv-lb-enter-active,
.dv-lb-leave-active {
  transition: opacity 0.2s ease;
}

.dv-lb-enter-from,
.dv-lb-leave-to {
  opacity: 0;
}

@media (max-width: 640px) {
  .dv-lb {
    padding: 64px 0 16px;
  }

  .dv-lb__frame--telephone {
    width: min(100%, calc((100vh - 150px) * 0.462));
    border-radius: 18px;
  }

  .dv-lb__caption {
    padding: 0 16px;
    font-size: 13px;
  }
}
</style>
