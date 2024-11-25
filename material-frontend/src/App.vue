<template>
  <div class="app-wrapper">
    <MaterialList 
      :materials="materials" 
      :selectedMaterial="selectedMaterial"
      @select-material="selectMaterial" 
    />
    <MaterialDetail :material="selectedMaterial" />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import MaterialList from './components/MaterialList.vue'
import MaterialDetail from './components/MaterialDetail.vue'

export default {
  name: 'App',
  components: {
    MaterialList,
    MaterialDetail
  },
  setup() {
    const materials = ref({})
    const selectedMaterial = ref(null)

    const fetchMaterials = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/materials')
        materials.value = await response.json()
      } catch (error) {
        console.error('Error fetching materials:', error)
      }
    }

    const selectMaterial = (material) => {
      selectedMaterial.value = material
    }

    onMounted(() => {
      fetchMaterials()
    })

    return {
      materials,
      selectedMaterial,
      selectMaterial
    }
  }
}
</script>

<style>
/* 重置默认样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

#app {
  height: 100vh;
  width: 100vw;
}

.app-wrapper {
  display: flex;
  height: 100%;
  width: 100%;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #f5f7fa;
}
</style>
