<script setup>
import { computed } from 'vue'

const props = defineProps({
  duel: { type: Object, required: true },
  wastePct: { type: Number, default: null },
  snapshot: { type: Boolean, default: false },
})

const largerLabel = computed(() => ({
  area: '面积法更大',
  grid: '网格更大',
  tie: '两侧持平',
}[props.duel.larger] || '未知'))
</script>
<template>
  <section class="duel-panel">
    <h2>面积法 vs 网格</h2>
    <div class="duel-sides">
      <div class="duel-side" :class="{ winner: duel.larger === 'area' }">
        <div class="duel-num">{{ duel.area_order_count }}</div>
        <div>面积法订货（片）</div>
      </div>
      <div class="duel-vs">VS</div>
      <div class="duel-side" :class="{ winner: duel.larger === 'grid' }">
        <div class="duel-num">{{ duel.grid_count }}</div>
        <div>矩形网格（块）</div>
      </div>
    </div>
    <p class="duel-verdict">
      差值 {{ duel.diff }} · <strong>{{ largerLabel }}</strong>
    </p>
    <p v-if="wastePct !== null" class="duel-snapshot">
      损耗 {{ wastePct }}%<span v-if="snapshot">（写入时取值）</span>
    </p>
  </section>
</template>
