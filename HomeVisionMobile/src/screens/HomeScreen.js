import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  RefreshControl,
  Alert,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import { apiService } from '../services/apiService';
import { useNotifications } from '../context/NotificationContext';

const HomeScreen = () => {
  const [systemStats, setSystemStats] = useState({
    totalCameras: 0,
    activeCameras: 0,
    totalEvents: 0,
    recentEvents: 0,
  });
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const { unreadCount } = useNotifications();

  useEffect(() => {
    loadSystemStats();
  }, []);

  const loadSystemStats = async () => {
    try {
      setLoading(true);
      
      // Load cameras
      const camerasResponse = await apiService.getCameras();
      const cameras = camerasResponse.data;
      
      // Load events
      const eventsResponse = await apiService.getEvents({ limit: 10 });
      const events = eventsResponse.data;
      
      setSystemStats({
        totalCameras: cameras.length,
        activeCameras: cameras.filter(c => c.is_active).length,
        totalEvents: events.length,
        recentEvents: events.filter(e => {
          const eventDate = new Date(e.created_at);
          const now = new Date();
          const diffHours = (now - eventDate) / (1000 * 60 * 60);
          return diffHours <= 24;
        }).length,
      });
    } catch (error) {
      console.error('Failed to load system stats:', error);
      Alert.alert('Error', 'Failed to load system statistics');
    } finally {
      setLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadSystemStats();
    setRefreshing(false);
  };

  const renderStatCard = ({ icon, title, value, color, subtitle }) => (
    <View style={styles.statCard}>
      <View style={[styles.statIcon, { backgroundColor: color }]}>
        <Icon name={icon} size={24} color="#FFFFFF" />
      </View>
      <View style={styles.statContent}>
        <Text style={styles.statValue}>{value}</Text>
        <Text style={styles.statTitle}>{title}</Text>
        {subtitle && <Text style={styles.statSubtitle}>{subtitle}</Text>}
      </View>
    </View>
  );

  const renderQuickAction = ({ icon, title, subtitle, onPress, color = '#2196F3' }) => (
    <TouchableOpacity style={styles.quickAction} onPress={onPress}>
      <View style={[styles.quickActionIcon, { backgroundColor: color }]}>
        <Icon name={icon} size={24} color="#FFFFFF" />
      </View>
      <View style={styles.quickActionContent}>
        <Text style={styles.quickActionTitle}>{title}</Text>
        <Text style={styles.quickActionSubtitle}>{subtitle}</Text>
      </View>
      <Icon name="chevron-right" size={20} color="#999" />
    </TouchableOpacity>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <Icon name="refresh" size={40} color="#2196F3" />
        <Text style={styles.loadingText}>Loading system status...</Text>
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
      showsVerticalScrollIndicator={false}
    >
      {/* Header */}
      <View style={styles.header}>
        <View>
          <Text style={styles.welcomeText}>Welcome back!</Text>
          <Text style={styles.statusText}>
            System Status: {systemStats.activeCameras > 0 ? 'Active' : 'Inactive'}
          </Text>
        </View>
        {unreadCount > 0 && (
          <View style={styles.notificationBadge}>
            <Text style={styles.notificationBadgeText}>{unreadCount}</Text>
          </View>
        )}
      </View>

      {/* System Stats */}
      <View style={styles.statsContainer}>
        <Text style={styles.sectionTitle}>System Overview</Text>
        <View style={styles.statsGrid}>
          {renderStatCard({
            icon: 'videocam',
            title: 'Cameras',
            value: `${systemStats.activeCameras}/${systemStats.totalCameras}`,
            color: '#2196F3',
            subtitle: 'Active/Total',
          })}
          {renderStatCard({
            icon: 'notifications',
            title: 'Notifications',
            value: unreadCount,
            color: '#FF9800',
            subtitle: 'Unread',
          })}
          {renderStatCard({
            icon: 'event',
            title: 'Events',
            value: systemStats.totalEvents,
            color: '#4CAF50',
            subtitle: 'Total',
          })}
          {renderStatCard({
            icon: 'schedule',
            title: 'Recent',
            value: systemStats.recentEvents,
            color: '#9C27B0',
            subtitle: 'Last 24h',
          })}
        </View>
      </View>

      {/* Quick Actions */}
      <View style={styles.quickActionsContainer}>
        <Text style={styles.sectionTitle}>Quick Actions</Text>
        <View style={styles.quickActionsList}>
          {renderQuickAction({
            icon: 'videocam',
            title: 'View Cameras',
            subtitle: 'Monitor all camera feeds',
            onPress: () => {
              // Navigate to cameras screen
              console.log('Navigate to cameras');
            },
          })}
          {renderQuickAction({
            icon: 'notifications',
            title: 'Notifications',
            subtitle: `${unreadCount} unread notifications`,
            onPress: () => {
              // Navigate to notifications screen
              console.log('Navigate to notifications');
            },
            color: unreadCount > 0 ? '#F44336' : '#2196F3',
          })}
          {renderQuickAction({
            icon: 'event',
            title: 'Recent Events',
            subtitle: 'View latest detection events',
            onPress: () => {
              // Navigate to events screen
              console.log('Navigate to events');
            },
          })}
          {renderQuickAction({
            icon: 'settings',
            title: 'Settings',
            subtitle: 'Configure system preferences',
            onPress: () => {
              // Navigate to settings screen
              console.log('Navigate to settings');
            },
          })}
        </View>
      </View>

      {/* System Status */}
      <View style={styles.statusContainer}>
        <Text style={styles.sectionTitle}>System Status</Text>
        <View style={styles.statusCard}>
          <View style={styles.statusRow}>
            <Icon name="wifi" size={20} color="#4CAF50" />
            <Text style={styles.statusText}>Network: Connected</Text>
          </View>
          <View style={styles.statusRow}>
            <Icon name="storage" size={20} color="#4CAF50" />
            <Text style={styles.statusText}>Storage: Available</Text>
          </View>
          <View style={styles.statusRow}>
            <Icon name="security" size={20} color="#4CAF50" />
            <Text style={styles.statusText}>Security: Active</Text>
          </View>
          <View style={styles.statusRow}>
            <Icon name="update" size={20} color="#4CAF50" />
            <Text style={styles.statusText}>System: Up to date</Text>
          </View>
        </View>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F5F5F5',
  },
  loadingText: {
    marginTop: 10,
    fontSize: 16,
    color: '#666',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 20,
    backgroundColor: '#FFFFFF',
  },
  welcomeText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 4,
  },
  statusText: {
    fontSize: 14,
    color: '#666',
  },
  notificationBadge: {
    backgroundColor: '#F44336',
    borderRadius: 12,
    paddingHorizontal: 8,
    paddingVertical: 4,
    minWidth: 24,
    alignItems: 'center',
  },
  notificationBadgeText: {
    color: '#FFFFFF',
    fontSize: 12,
    fontWeight: 'bold',
  },
  statsContainer: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  statCard: {
    width: '48%',
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 15,
    marginBottom: 15,
    flexDirection: 'row',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  statIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  statContent: {
    flex: 1,
  },
  statValue: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 2,
  },
  statTitle: {
    fontSize: 14,
    color: '#666',
  },
  statSubtitle: {
    fontSize: 12,
    color: '#999',
  },
  quickActionsContainer: {
    padding: 20,
  },
  quickActionsList: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  quickAction: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#F0F0F0',
  },
  quickActionIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 15,
  },
  quickActionContent: {
    flex: 1,
  },
  quickActionTitle: {
    fontSize: 16,
    fontWeight: '500',
    color: '#333',
    marginBottom: 2,
  },
  quickActionSubtitle: {
    fontSize: 12,
    color: '#666',
  },
  statusContainer: {
    padding: 20,
    paddingBottom: 40,
  },
  statusCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 15,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  statusRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 8,
  },
  statusText: {
    fontSize: 14,
    color: '#333',
    marginLeft: 10,
  },
});

export default HomeScreen; 