<template>
  <div class="detail-container" v-if="material">
    <div class="material-header">
      <h1>{{ material.Material.Name }}</h1>
      <div class="material-aliases" v-if="material.Material.OldName || material.Material.OtherNames?.length">
        <span v-if="material.Material.OldName">旧称: {{ material.Material.OldName }}</span>
        <span v-if="material.Material.OtherNames?.length">
          其他名称: {{ material.Material.OtherNames.join(', ') }}
        </span>
      </div>
    </div>

    <el-card class="info-section">
      <template #header>
        <div class="card-header">
          <span>基本信息</span>
        </div>
      </template>
      <div class="info-grid">
        <div class="info-item">
          <label>分类</label>
          <span>{{ material.Material.Category }}</span>
        </div>
        <div class="info-item">
          <label>密度</label>
          <span>{{ material.Material.Density || '-' }}</span>
        </div>
        <div class="info-item description">
          <label>描述</label>
          <span>{{ material.Material.Description }}</span>
        </div>
      </div>
    </el-card>

    <el-card class="info-section">
      <template #header>
        <div class="card-header">
          <span>标准信息</span>
        </div>
      </template>
      <div class="standard-info">
        <h4>所属标准</h4>
        <div class="standard-item" v-if="material.Material.BelongsToStandard">
          <span class="standard-code">{{ material.Material.BelongsToStandard.StandardCode }}</span>
          <span class="standard-desc">{{ material.Material.BelongsToStandard.Description }}</span>
        </div>
        
        <h4>相关标准</h4>
        <div class="standard-list">
          <div v-for="(standard, index) in material.Material.AllStandards" 
               :key="index" 
               class="standard-item">
            <span class="standard-code">{{ standard.StandardCode }}</span>
            <span class="standard-desc">{{ standard.Description }}</span>
          </div>
        </div>
      </div>
    </el-card>

    <el-card class="info-section">
      <template #header>
        <div class="card-header">
          <span>化学成分</span>
        </div>
      </template>
      <el-table :data="chemicalComposition" stripe style="width: 100%">
        <el-table-column prop="element" label="元素" width="100" />
        <el-table-column prop="min" label="最小值 (%)" width="120" />
        <el-table-column prop="max" label="最大值 (%)" width="120" />
      </el-table>
      <div class="composition-notes" v-if="material.ChemicalComposition.Notes">
        <h4>备注：</h4>
        <ul>
          <li v-for="(note, index) in material.ChemicalComposition.Notes" 
              :key="index">{{ note }}</li>
        </ul>
      </div>
    </el-card>

    <el-card class="info-section">
      <template #header>
        <div class="card-header">
          <span>机械性能</span>
        </div>
      </template>
      <el-tabs>
        <el-tab-pane label="性能条件">
          <el-table :data="material.MechanicalProperties.Conditions" stripe>
            <el-table-column prop="Property" label="性能" />
            <el-table-column prop="Condition" label="条件" />
            <el-table-column prop="Value" label="数值" />
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="热处理工艺">
          <el-table :data="material.MechanicalProperties.HeatTreatment" stripe>
            <el-table-column prop="Process" label="工艺" />
            <el-table-column prop="TemperatureRange" label="温度范围" />
            <el-table-column prop="CoolingMethod" label="冷却方式" />
          </el-table>
        </el-tab-pane>
      </el-tabs>
      <div class="mechanical-notes" v-if="material.MechanicalProperties.Notes">
        <h4>备注：</h4>
        <ul>
          <li v-for="(note, index) in material.MechanicalProperties.Notes" 
              :key="index">{{ note }}</li>
        </ul>
      </div>
    </el-card>

    <el-card class="info-section" v-if="material.PhysicalProperties.Properties.length">
      <template #header>
        <div class="card-header">
          <span>物理性能</span>
        </div>
      </template>
      <el-table :data="material.PhysicalProperties.Properties" stripe>
        <el-table-column prop="Property" label="性能" />
        <el-table-column prop="Value" label="数值" />
        <el-table-column prop="Unit" label="单位" />
      </el-table>
    </el-card>

    <el-card class="info-section" v-if="material.SimilarGrades">
      <template #header>
        <div class="card-header">
          <span>相似牌号</span>
        </div>
      </template>
      <div v-for="(field, fieldIndex) in material.SimilarGrades" :key="fieldIndex" class="similar-grades-field">
        <h4>{{ field.Field }}</h4>
        <el-table :data="field.Mappings" stripe>
          <el-table-column prop="Standard" label="标准" width="120" />
          <el-table-column label="牌号">
            <template #default="scope">
              {{ scope.row.Grades.join(', ') }}
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
  </div>
  <div v-else class="empty-state">
    <el-empty description="请选择一个材料查看详细信息" />
  </div>
</template>

<script>
export default {
  name: 'MaterialDetail',
  props: {
    material: {
      type: Object,
      default: null
    }
  },
  computed: {
    chemicalComposition() {
      if (!this.material?.ChemicalComposition?.Elements) return []
      
      return Object.entries(this.material.ChemicalComposition.Elements).map(([element, values]) => ({
        element,
        min: values.Min || '-',
        max: values.Max || '-'
      }))
    }
  }
}
</script>

<style scoped>
.detail-container {
  flex: 1;
  padding: 24px;
  background: #f5f7fa;
  overflow-y: auto;
}

.material-header {
  margin-bottom: 24px;
}

.material-header h1 {
  color: #303133;
  font-size: 28px;
  margin: 0 0 8px 0;
}

.material-aliases {
  color: #909399;
  font-size: 14px;
}

.material-aliases span {
  margin-right: 16px;
}

.info-section {
  margin-bottom: 24px;
}

.info-section:last-child {
  margin-bottom: 0;
}

.card-header {
  display: flex;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
  color: #303133;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
}

.info-item.description {
  grid-column: 1 / -1;
}

.info-item label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.info-item span {
  font-size: 16px;
  color: #303133;
}

.standard-info h4,
.similar-grades-field h4 {
  margin: 16px 0 8px 0;
  color: #606266;
}

.standard-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  padding: 8px;
  background: #f5f7fa;
  border-radius: 4px;
}

.standard-code {
  font-weight: bold;
  margin-right: 12px;
  color: #409eff;
}

.composition-notes,
.mechanical-notes {
  margin-top: 16px;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 4px;
}

.composition-notes h4,
.mechanical-notes h4 {
  margin: 0 0 8px 0;
  color: #606266;
}

.composition-notes ul,
.mechanical-notes ul {
  margin: 0;
  padding-left: 20px;
}

.composition-notes li,
.mechanical-notes li {
  color: #606266;
  margin-bottom: 4px;
}

.similar-grades-field {
  margin-bottom: 20px;
}

.empty-state {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f5f7fa;
}

:deep(.el-card__header) {
  padding: 16px 20px;
  border-bottom: 1px solid #e4e7ed;
  background: #ffffff;
}

:deep(.el-card__body) {
  padding: 20px;
}

:deep(.el-table) {
  margin-bottom: 16px;
}

:deep(.el-tabs__header) {
  margin-bottom: 16px;
}
</style> 