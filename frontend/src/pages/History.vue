<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
import DuelPanel from '../components/DuelPanel.vue'

const items = ref([])
const detail = ref(null)
const err = ref('')

onMounted(async () => { items.value = (await getJSON('/api/runs')).items })

// 对决数字一律取自写入时的 result；旧记录无内嵌 duel 时用同一 payload 里的两侧数字补出
function duelOf(run) {
  const r = run?.result
  if (!r) return null
  if (r.duel) return r.duel
  if (r.layout && r.order_count != null) {
    const area = r.order_count
    const grid = r.layout.grid_count
    return {
      area_order_count: area,
      grid_count: grid,
      diff: Math.abs(area - grid),
      larger: area > grid ? 'area' : grid > area ? 'grid' : 'tie',
    }
  }
  return null
}

async function open(run) {
  err.value = ''
  try {
    detail.value = await getJSON(`/api/runs/${run.id}`)
  } catch (e) {
    err.value = e.message
    detail.value = null
  }
}
</script>
<template>
  <div class="page">
    <h1>测算记录</h1>
    <table class="tbl tbl-clickable">
      <thead><tr><th>时间</th><th>房间</th><th>砖型</th><th>片数</th><th>对决（面积/网格）</th></tr></thead>
      <tbody>
        <tr v-for="r in items" :key="r.id" @click="open(r)">
          <td>{{ r.created_at?.slice(0, 19) }}</td>
          <td>{{ r.room_name }}</td>
          <td>{{ r.tile_name }}</td>
          <td>{{ r.result?.order_count }}</td>
          <td>
            <template v-if="duelOf(r)">{{ duelOf(r).area_order_count }} / {{ duelOf(r).grid_count }}</template>
            <template v-else>—</template>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-if="err" class="alert">{{ err }}</p>
    <section v-if="detail" class="run-detail">
      <h2>记录 #{{ detail.id }} · {{ detail.room_name }} × {{ detail.tile_name }}</h2>
      <p>保存于 {{ detail.created_at?.slice(0, 19) }}<template v-if="detail.note"> · 备注：{{ detail.note }}</template></p>
      <div class="bench-panels">
        <DuelPanel v-if="duelOf(detail)" :duel="duelOf(detail)" :waste-pct="detail.waste_pct" :snapshot="true" />
        <p v-else class="alert">该记录不含对决数据</p>
      </div>
    </section>
  </div>
</template>
