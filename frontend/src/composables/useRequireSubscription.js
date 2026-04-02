import { useRouter, useRoute } from 'vue-router'
import { useSubscriptionStore } from '@/stores/subscription'
import { useUserStore } from '@/stores/user'

/**
 * Helper composable to ensure the current user has subscription access.
 * If access is missing, redirects to the billing page with a redirect param.
 */
export function useRequireSubscription() {
  const router = useRouter()
  const route = useRoute()
  const subscriptionStore = useSubscriptionStore()
  const userStore = useUserStore()

  const ensureAccess = async (targetRoute = null) => {
    if (userStore.isAdmin) {
      return true
    }

    const currentLevelId = userStore.niveau_pays?.id

    try {
      await subscriptionStore.fetchStatus({ force: true })
    } catch (e) {
      // ignore: we'll redirect below if access still absent
    }

    if (!subscriptionStore.accessForLevel(currentLevelId)) {
      try {
        await subscriptionStore.refreshUntilLevelAccess(currentLevelId, { attempts: 2, interval: 1000 })
      } catch (e) {
        // ignore and redirect below
      }
    }

    if (subscriptionStore.accessForLevel(currentLevelId)) {
      return true
    }

    const resolved = targetRoute
      ? router.resolve(targetRoute).fullPath
      : route.fullPath

    router.push({
      name: 'Billing',
      query: {
        redirect: resolved,
        reason: 'subscription_required'
      }
    })
    return false
  }

  return { ensureAccess }
}
