<template>
  <header class="navbar-top">
    <nav>
      <ul class="nav-list">
        <li v-for="(label, path) in navItems" :key="path">
          <router-link
            :to="path"
            class="nav-link"
            :class="{
              'active': $route.path === path
            }"
          >
            {{ label }}
          </router-link>
        </li>
      </ul>
    </nav>
  </header>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { navItems } from '@/components/navigation/navItems.js' 

const route = useRoute()
</script>

<style scoped>
.nav-link,
.nav-link:visited,
.nav-link:focus,
.nav-link:active {
  color: white !important;
  text-decoration: none;
}


.navbar-top {
  position: absolute;
  justify-content: center;
  width: 100%;
  z-index: 1000;
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  background: rgba(0, 0, 0, 0);
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
}

.nav-list {
  list-style: none;
  display: flex;
  gap: 1.5rem;
}

.nav-link {
  text-decoration: none;
  color: white;
  transition: all 0.3s ease;
}

.nav-link:hover {
  text-decoration: none;
  color: white;
  text-decoration: underline;
}

.nav-link.active {
  color: #ffffff;
  padding: 0.3rem 0.7rem;
  border-radius: 5px;
  font-weight: bold;
}
</style>
