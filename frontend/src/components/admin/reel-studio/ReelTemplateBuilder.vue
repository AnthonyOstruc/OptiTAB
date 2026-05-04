<template>
  <section class="template-builder">
    <div class="template-header">
      <h3>Création Reel</h3>
    </div>

    <form class="template-form" @submit.prevent="handleSubmit">
      <label>
        Format / Script (par slides)
        <textarea
          v-model="form.template_text"
          rows="13"
          maxlength="12000"
          placeholder="MODE AUTO (IA décide le nombre de slides)&#10;TITLE: Dérivation produit&#10;HOOK: Défi bac&#10;f(x)=x\ln(x)&#10;u=x \qquad v=\ln(x)&#10;u'=1 \qquad v'=\frac{1}{x}&#10;f'(x)=\ln(x)+1&#10;CTA: Abonne-toi à OptiTAB | Sauvegarde ce Reel | Commente ton résultat&#10;&#10;OU MODE MANUEL:&#10;SLIDE 1 | hook&#10;TITLE: Défi bac&#10;KATEX: f(x)=x\ln(x)&#10;TEXT: Tu trouves combien ?&#10;---&#10;SLIDE 2 | katex&#10;TEXT: Correction :&#10;KATEX: f(x)=x\ln(x)&#10;---&#10;SLIDE 3 | cta&#10;TITLE: Résultat&#10;KATEX: f'(x)=\ln(x)+1&#10;TEXT: Abonne-toi à OptiTAB&#10;Sauvegarde ce Reel&#10;Commente ton résultat"
        ></textarea>
      </label>

      <button class="btn-primary" type="submit" :disabled="disabled || loading || !canSubmit">
        {{ loading ? 'Génération...' : 'Générer depuis template' }}
      </button>
    </form>
  </section>
</template>

<script setup>
import { computed, reactive } from 'vue'

const props = defineProps({
  loading: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['generate'])

const form = reactive({
  template_text: '',
})

const canSubmit = computed(() => String(form.template_text || '').trim().length > 0)

function handleSubmit() {
  if (!canSubmit.value) return

  emit('generate', {
    template_text: String(form.template_text || '').trim(),
  })
}
</script>

<style scoped>
.template-builder {
  border: 1px solid #dbe4ee;
  border-radius: 12px;
  background: #ffffff;
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.template-header h3 {
  margin: 0;
  color: #193e8e;
  font-size: 18px;
}

.template-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding-bottom: 8px;
}

label {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 13px;
  font-weight: 700;
  color: #334155;
}

input,
textarea {
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 10px 12px;
  font-size: 14px;
  color: #0f172a;
  background: #fff;
  font-family: inherit;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

.btn-primary {
  align-self: flex-start;
  border: 0;
  border-radius: 8px;
  padding: 10px 14px;
  background: #1d4ed8;
  color: #ffffff;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}

.btn-primary:disabled {
  background: #94a3b8;
  cursor: not-allowed;
}

</style>
