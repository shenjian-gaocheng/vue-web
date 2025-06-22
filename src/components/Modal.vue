<template>
  <div v-if="modelValue" class="modal-mask">
    <div class="modal-container">
      <h3 class="modal-title">{{ title }}</h3>
      <div class="modal-body">
        <slot />
      </div>
      <div class="modal-footer">
        <button class="btn" @click="close">取消</button>
        <button class="btn btn-primary" @click="confirm">确认</button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: Boolean,
  title: { type: String, default: '提示' }
})
const emit = defineEmits(['update:modelValue', 'confirm'])

const close = () => emit('update:modelValue', false)
const confirm = () => emit('confirm')

</script>

<style scoped>
.modal-mask {
  position: fixed;
  z-index: 9997;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-container {
  background: white;
  border-radius: 8px;
  width: 800px;
  max-width: 100%;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}
.modal-title {
  margin-top: 0;
  margin-bottom: 1rem;
}
.modal-body {
  max-height: 70vh; /* 限制高度为视口的60%，你可以调整这个值 */
  overflow-y: auto;
}
.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 1.5rem;
}
.btn {
  padding: 0.4rem 1rem;
  border: none;
  background: #ddd;
  border-radius: 4px;
  cursor: pointer;
}
.btn-primary {
  background: #409eff;
  color: white;
}
</style>