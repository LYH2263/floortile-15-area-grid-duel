<script setup>
import { computed } from 'vue'

const props = defineProps({
  showdown: { type: Object, default: null },
})

const SIDE_LABELS = { area: '面积法', grid: '矩形网格', tie: '两侧持平' }
const largerLabel = computed(() => SIDE_LABELS[props.showdown?.larger_side] || '—')
</script>
<template>
  <section v-if="showdown" class="showdown">
    <h2>面积法 vs 网格 对决</h2>
    <div class="showdown-sides">
      <div class="side" :class="{ winner: showdown.larger_side === 'area' }">
        <h3>面积法订货</h3>
        <div class="hero">{{ showdown.area.order_count }} 片</div>
        <p>净用量 {{ showdown.area.raw_count }} 片 · 损耗 {{ showdown.area.waste_pct }}%</p>
      </div>
      <div class="vs">VS</div>
      <div class="side" :class="{ winner: showdown.larger_side === 'grid' }">
        <h3>矩形网格</h3>
        <div class="hero">{{ showdown.grid.grid_count }} 块</div>
        <p>{{ showdown.grid.cols }} 列 × {{ showdown.grid.rows }} 行</p>
      </div>
    </div>
    <p class="diff">差值 {{ showdown.diff }} 片 · 更大侧：{{ largerLabel }}</p>
  </section>
</template>
