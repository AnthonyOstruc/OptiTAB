<script setup>
import { computed } from 'vue'

const props = defineProps({
  testimonial: { type: Object, required: true }
})

defineEmits(['open'])

const isWhatsapp = computed(() => props.testimonial.channel !== 'sms')
const channelLabel = computed(() => (isWhatsapp.value ? 'WhatsApp' : 'SMS'))

// Anonyme par défaut. `name` n'est renseigné par l'API que si la personne
// a explicitement autorisé l'affichage de son prénom ; sinon on retombe sur
// le profil (« Maman d'élève »), puis sur le niveau.
const primaryLabel = computed(
  () => props.testimonial.name || props.testimonial.author || props.testimonial.role || 'Témoignage'
)

const secondaryLabel = computed(() => {
  const { name, author, role } = props.testimonial
  if (name) return [author, role].filter(Boolean).join(' · ')
  return author ? role : ''
})
</script>

<template>
  <button
    type="button"
    class="shot"
    :aria-label="`Agrandir la capture : ${primaryLabel}`"
    @click="$emit('open', testimonial)"
  >
    <!-- Cadre a ratio fixe : toutes les cartes ont exactement la meme hauteur,
         quelle que soit la taille de la capture d'origine.
         L'image est en `contain` : elle est TOUJOURS montree en entier, jamais
         recadree de travers. Le vide est comble par la meme image floutee, ce
         qui remplit le cadre sans bandes mortes — et fonctionne aussi bien
         pour une capture large que pour une capture verticale. -->
    <span class="shot__frame">
      <img :src="testimonial.src" class="shot__backdrop" alt="" aria-hidden="true" />
      <img
        :src="testimonial.src"
        :alt="testimonial.alt || `Capture ${channelLabel} — ${primaryLabel}`"
        class="shot__img"
        loading="lazy"
        decoding="async"
      />
      <span class="shot__zoom" aria-hidden="true">
        <svg viewBox="0 0 24 24">
          <circle cx="11" cy="11" r="6.5" fill="none" stroke="currentColor" stroke-width="1.9" />
          <path
            d="M15.8 15.8 20 20M11 8.6v4.8M8.6 11h4.8"
            fill="none"
            stroke="currentColor"
            stroke-width="1.9"
            stroke-linecap="round"
          />
        </svg>
      </span>
    </span>

    <span class="shot__meta">
      <span class="shot__identity">
        <span class="shot__author">{{ primaryLabel }}</span>
        <span v-if="secondaryLabel" class="shot__role">{{ secondaryLabel }}</span>
      </span>
      <span class="shot__channel" :class="isWhatsapp ? 'is-wa' : 'is-sms'">
        <svg v-if="isWhatsapp" viewBox="0 0 24 24" aria-hidden="true">
          <path
            fill="currentColor"
            d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.28-1.38a9.87 9.87 0 0 0 4.71 1.2h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2Zm4.52 11.99c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.24-.64.8-.78.97-.15.16-.29.18-.53.06-.25-.12-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.01-.38.11-.5.11-.11.25-.29.37-.43.13-.15.17-.25.25-.41.08-.17.04-.31-.02-.43-.06-.12-.56-1.34-.76-1.84-.2-.48-.4-.42-.56-.43h-.48c-.16 0-.43.06-.65.31-.22.25-.85.83-.85 2.03s.87 2.35.99 2.51c.12.16 1.71 2.61 4.14 3.66.58.25 1.03.4 1.38.51.58.19 1.11.16 1.53.1.47-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.15-1.18-.06-.1-.22-.16-.47-.28Z"
          />
        </svg>
        <svg v-else viewBox="0 0 24 24" aria-hidden="true">
          <path
            fill="currentColor"
            d="M20 2H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h3v3.2a.8.8 0 0 0 1.3.62L13 18h7a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2Z"
          />
        </svg>
        <span class="shot__channel-label">{{ channelLabel }}</span>
      </span>
    </span>
  </button>
</template>

<style scoped lang="scss">
.shot {
  display: flex;
  flex-direction: column;
  width: 100%;
  padding: 0;
  border-radius: 14px;
  border: 1px solid #d6e1ff;
  background: #ffffff;
  font-family: inherit;
  text-align: left;
  cursor: pointer;
  overflow: hidden;
  transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
}

.shot:hover {
  transform: translateY(-2px);
  border-color: #a8c1ff;
  box-shadow: 0 10px 24px rgba(30, 58, 138, 0.1);
}

.shot:focus-visible {
  outline: 2px solid #2a38b7;
  outline-offset: 2px;
}

/* Ratio fixe = grille parfaitement alignee, aucune carte plus haute qu'une autre.
   4/3 : la plupart des captures de conversation sont plus larges que hautes. */
.shot__frame {
  position: relative;
  display: block;
  width: 100%;
  aspect-ratio: 4 / 3;
  background: #eef2f7;
  overflow: hidden;
}

/* Fond : la meme image, floutee et agrandie, pour remplir le cadre sans
   bandes vides. Purement decoratif, masque aux lecteurs d'ecran. */
.shot__backdrop {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: blur(16px) saturate(1.15);
  transform: scale(1.2);
  opacity: 0.55;
  pointer-events: none;
}

/* La capture elle-meme, entiere et jamais deformee. */
.shot__img {
  position: relative;
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
}

.shot__zoom {
  position: absolute;
  right: 8px;
  bottom: 8px;
  width: 30px;
  height: 30px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.94);
  color: #1e3a8a;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.16);
  opacity: 0;
  transition: opacity 0.2s ease;

  svg {
    width: 16px;
    height: 16px;
  }
}

.shot:hover .shot__zoom,
.shot:focus-visible .shot__zoom {
  opacity: 1;
}

.shot__meta {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 11px 13px;
  border-top: 1px solid #e2e9fb;
}

.shot__identity {
  display: flex;
  flex-direction: column;
  min-width: 0;
  flex: 1;
}

/* Une seule ligne garantie : sans cela un profil long passe sur deux lignes
   et la carte devient plus haute que ses voisines. */
.shot__author {
  font-size: 0.92rem;
  font-weight: 800;
  color: #0f172a;
  line-height: 1.25;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.shot__role {
  font-size: 0.78rem;
  color: #475569;
  line-height: 1.3;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.shot__channel {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  min-height: 24px;
  padding: 0 9px;
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 700;

  svg {
    width: 12px;
    height: 12px;
  }

  &.is-wa {
    background: #e7f8ec;
    border: 1px solid #bfe8cd;
    color: #128c4a;
  }

  &.is-sms {
    background: #eef4ff;
    border: 1px solid #cfe0ff;
    color: #1e3a8a;
  }
}

/* Sur carte etroite, le libelle du badge mange la place du profil.
   On garde l'icone seule : le canal reste identifiable, le nom respire. */
@media (max-width: 700px) {
  .shot__channel {
    padding: 0 6px;
  }

  .shot__channel-label {
    display: none;
  }
}

@media (prefers-reduced-motion: reduce) {
  .shot {
    transition: none;
  }

  .shot:hover {
    transform: none;
  }

  .shot__zoom {
    opacity: 1;
    transition: none;
  }
}
</style>
