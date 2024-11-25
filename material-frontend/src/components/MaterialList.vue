<template>
  <div class="material-list">
    <div class="list-header">
      <h2>材料列表</h2>
      <div class="material-count">共 {{ Object.keys(materials).length }} 个材料</div>
    </div>

    <div class="search-box">
      <el-input
        v-model="searchQuery"
        placeholder="搜索材料..."
        clearable
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
    </div>

    <div class="materials-container">
      <el-scrollbar>
        <el-collapse v-model="activeNames">
          <el-collapse-item
            v-for="(versions, materialName) in filteredMaterials"
            :key="materialName"
            :title="materialName"
            :name="materialName"
          >
            <template #title>
              <div class="material-title">
                <span>{{ materialName }}</span>
                <span class="material-category">{{ versions[0].data.Material.Category }}</span>
              </div>
            </template>
            
            <div
              v-for="(version, index) in versions"
              :key="index"
              class="standard-item"
              :class="{ active: isSelected(version.data) }"
              @click="$emit('select-material', version.data)"
            >
              <div class="standard-info">
                <span class="standard-code">{{ version.standard }}</span>
                <span class="standard-desc">{{ version.description }}</span>
              </div>
            </div>
          </el-collapse-item>
        </el-collapse>
      </el-scrollbar>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { Search } from '@element-plus/icons-vue'

export default {
  name: 'MaterialList',
  components: {
    Search
  },
  props: {
    materials: {
      type: Object,
      default: () => ({})
    },
    selectedMaterial: {
      type: Object,
      default: null
    }
  },
  setup(props) {
    const searchQuery = ref('')
    const activeNames = ref([]) // 用于控制折叠面板的展开状态

    const filteredMaterials = computed(() => {
      const query = searchQuery.value.toLowerCase()
      if (!query) return props.materials

      const filtered = {}
      for (const [name, versions] of Object.entries(props.materials)) {
        if (
          name.toLowerCase().includes(query) ||
          versions.some(v => 
            v.standard.toLowerCase().includes(query) ||
            v.description.toLowerCase().includes(query) ||
            v.data.Material.Category.toLowerCase().includes(query)
          )
        ) {
          filtered[name] = versions
        }
      }
      return filtered
    })

    const isSelected = (material) => {
      return props.selectedMaterial?.Material?.Name === material.Material.Name &&
             props.selectedMaterial?.Material?.BelongsToStandard?.StandardCode === 
             material.Material.BelongsToStandard?.StandardCode
    }

    return {
      searchQuery,
      filteredMaterials,
      activeNames,
      isSelected
    }
  }
}
</script>

<style scoped>
.material-list {
  width: 300px;
  height: 100%;
  background: #ffffff;
  border-right: 1px solid #e4e7ed;
  display: flex;
  flex-direction: column;
}

.list-header {
  padding: 20px;
  border-bottom: 1px solid #e4e7ed;
}

.list-header h2 {
  margin: 0;
  font-size: 20px;
  color: #303133;
}

.material-count {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}

.search-box {
  padding: 16px;
  border-bottom: 1px solid #e4e7ed;
}

.materials-container {
  flex: 1;
  overflow: hidden;
}

.material-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.material-category {
  font-size: 12px;
  color: #909399;
}

.standard-item {
  padding: 12px 16px;
  cursor: pointer;
  border-radius: 4px;
  margin: 4px 0;
  transition: all 0.3s ease;
}

.standard-item:hover {
  background: #f5f7fa;
}

.standard-item.active {
  background: #ecf5ff;
  border-right: 3px solid #409eff;
}

.standard-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.standard-code {
  font-size: 14px;
  color: #409eff;
}

.standard-desc {
  font-size: 12px;
  color: #909399;
}

:deep(.el-collapse) {
  border: none;
}

:deep(.el-collapse-item__header) {
  padding: 0 16px;
}

:deep(.el-collapse-item__content) {
  padding: 0 16px;
}

:deep(.el-scrollbar__wrap) {
  overflow-x: hidden;
}
</style> 