<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
import ShowdownCompare from '../components/ShowdownCompare.vue'

const items = ref([])
const detail = ref(null)
const err = ref('')

onMounted(async () => { items.value = (await getJSON('/api/runs')).items })

async function openRun(id) {
  err.value = ''
  try {
    detail.value = await getJSON(`/api/runs/${id}`)
  } catch (e) {
    err.value = e.message
    detail.value = null
  }
}
</script>
<template>
  <div class="page">
    <h1>测算记录</h1>
    <table class="tbl">
      <thead><tr><th>时间</th><th>房间</th><th>砖型</th><th>面积法片数</th><th>网格块数</th><th>差值</th><th></th></tr></thead>
      <tbody>
        <tr v-for="r in items" :key="r.id">
          <td>{{ r.created_at?.slice(0, 19) }}</td>
          <td>{{ r.room_name }}</td>
          <td>{{ r.tile_name }}</td>
          <td>{{ r.result?.showdown?.area?.order_count ?? r.result?.order_count }}</td>
          <td>{{ r.result?.showdown?.grid?.grid_count ?? '—' }}</td>
          <td>{{ r.result?.showdown?.diff ?? '—' }}</td>
          <td><button @click="openRun(r.id)">对决</button></td>
        </tr>
      </tbody>
    </table>
    <p v-if="err" class="alert">{{ err }}</p>
    <section v-if="detail" class="run-detail">
      <h2>记录 #{{ detail.id }} · {{ detail.room_name }} × {{ detail.tile_name }}</h2>
      <p>保存于 {{ detail.created_at?.slice(0, 19) }} · 损耗 {{ detail.waste_pct }}%（写入时取值，后续改默认损耗不影响本记录）</p>
      <ShowdownCompare v-if="detail.result?.showdown" :showdown="detail.result.showdown" />
      <p v-else>该记录保存于对决功能上线前，未内嵌两侧数字。</p>
    </section>
  </div>
</template>
